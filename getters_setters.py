import sublime
import sublime_plugin
import re

class GettersSettersCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		print('getters setters plugin called')
		#window = self.window
		#view = window.active_view()
		view = self.view
		print(view.sel()[0])
		currentLine = view.substr(view.line(view.sel()[0]))

		print(currentLine)
		result = re.search(r"\* @([a-zA-Z]+)\.inject", currentLine)
		if result:
			serviceName = result.group(1)
			print(serviceName)

			fullText = view.substr(sublime.Region(0, view.size()))
			initFunctionIndex = fullText.find("function init(")

			initOpeningBracketIndex = fullText.find( "(", initFunctionIndex )
			initClosingBracketIndex = fullText.find( ")", initOpeningBracketIndex )

			initBetweenBracketsResult = re.search(r"any function init\(([^()]*)\)", fullText )
			initBetweenBrackets = initBetweenBracketsResult.group(1)
			comma = "  "
			if not initBetweenBrackets.isspace():
				comma = ", "
			parameterText = "\t\t" + comma + "required any " + serviceName +"\n"

			view.insert(edit, initClosingBracketIndex-1, parameterText )
			# get fullText again as indexing will have changed
			fullText = view.substr(sublime.Region(0, view.size()))
			initReturnThisIndex = fullText.find( "return this;", initOpeningBracketIndex )
			initSetterText = "_set" + serviceName.title() + "( arguments." + serviceName + " );\n\t\t"
			view.insert(edit, initReturnThisIndex, initSetterText )

			fullText = view.substr(sublime.Region(0, view.size()))

			lastBraceIndex = fullText.rindex( "}" )

			getterText = "\tprivate any function _get" + serviceName.title() + "() {\n"
			getterText += "\t\treturn _" + serviceName + ";\n"
			getterText += "\t}"

			setterText = "\tprivate void function _set" + serviceName.title() + "( required any " + serviceName + " ) {\n"
			setterText += "\t\t_" + serviceName + " = arguments." + serviceName + ";\n"
			setterText += "\t}\n"

			view.insert(edit, lastBraceIndex, getterText + "\n" + setterText )