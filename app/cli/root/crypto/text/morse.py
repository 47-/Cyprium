#! /usr/bin/python3

########################################################################
#                                                                      #
#   Cyprium is a multifunction cryptographic, steganographic and       #
#   cryptanalysis tool developped by members of The Hackademy.         #
#   French White Hat Hackers Community!                                #
#   www.thehackademy.fr                                                #
#   Copyright © 2012                                                   #
#   Authors: SAKAROV, Madhatter, mont29, Luxerails, PauseKawa, fred,   #
#   afranck64, Tyrtamos.                                               #
#   Contact: cyprium@thehackademy.fr, sakarov@thehackademy.fr,         #
#   madhatter@thehackademy.fr, mont29@thehackademy.fr,                 #
#   irc.thehackademy.fr #cyprium, irc.thehackademy.fr #hackademy       #
#                                                                      #
#   Cyprium is free software: you can redistribute it and/or modify    #
#   it under the terms of the GNU General Public License as published  #
#   by the Free Software Foundation, either version 3 of the License,  #
#   or any later version.                                              #
#                                                                      #
#   This program is distributed in the hope that it will be useful,    #
#   but without any warranty; without even the implied warranty of     #
#   merchantability or fitness for a particular purpose. See the       #
#   GNU General Public License for more details.                       #
#                                                                      #
#   The terms of the GNU General Public License is detailed in the     #
#   COPYING attached file. If not, see : http://www.gnu.org/licenses   #
#                                                                      #
########################################################################


# In case we directly run that file, we need to add the whole cyprium to path,
# to get access to CLI stuff!
if __name__ == "__main__":
    import sys
    import os
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                 "..", "..", "..", "..",
                                                 "..")))

import app.cli
import kernel.crypto.text.morse as morse


class Morse(app.cli.Tool):
    """CLI wrapper for morse crypto text tool."""
    def main(self, ui):
        ui.message("********** Welcome to Cyprium.Morse! **********")
        quit = False
        while not quit:
            options = [(self.about, "*about", "Show some help!"),
                       (self.demo, "*demo", "Show some examples"),
                       (self.cypher, "*cypher",
                                     "Cypher some textual data in morse"),
                       (self.decypher, "d*ecypher",
                                       "Decypher morse into text"),
                       ("tree", "*tree", "Show the whole tree"),
                       ("quit", "*quit", "Quit Cyprium.Morse")]
            msg = "Cyprium.Morse"
            answ = ui.get_choice(msg, options, oneline=True)

            if answ == 'tree':
                self._tree.print_tree(ui, self._tree.FULL)
            elif answ == 'quit':
                self._tree.current = self._tree.current.parent
                quit = True
            else:
                answ(ui)
        ui.message("Back to Cyprium menus! Bye.")

    def about(self, ui):
        ui.message(morse.__about__)
        ui.get_choice("", [("", "Go back to *menu", "")], oneline=True)

    def demo(self, ui):
        sample = "Vancouver! Vancouver! This is it!"
        ui.message("===== Demo Mode =====")
        ui.message("Running a small demo/testing!")

        ui.message("--- Encoding ---")
        result = morse.cypher(sample)
        ui.message("Cypherd data in international morse:\n{}"
                   "".format(result))
        result = morse.cypher(sample, fast='true')
        ui.message("Cypherd data in fast international morse:\n{}"
                   "".format(result))
        tresult = morse.decypher(result)
        ui.message("--- Decoding ---")
        ui.message("And, finally, the decypherd data:\n{}".format(tresult))


        ui.get_choice("", [("", "Go back to *menu", "")], oneline=True)

    def cypher(self, ui):
        """Interactive version of cypher()."""
        txt = ""
        ui.message("===== Cypher Mode =====")

        while 1:
            done = False
            while 1:
                txt = ui.text_input("Text to cypher to Morse")
                if txt is None:
                    break  # Go back to main Cypher menu.

                try:
                    # Will also raise an exception if data is None.
                    fast = ui.get_data("Type the morse style you want to use (e.g. "
                                        "international, fast), or leave empty to use "
                                        "default international morse: ")
                    if not fast or fast == 'international':
                        fast = 'false'
                    elif fast == 'fast':
                        fast = 'true'
                    else:
                        # TODO: Analyser le texte pour faire un dico de décodage <<<<<<<
                        ui.message("Well done... but i try with the international code")
                        fast = 'false'
                    txt = morse.cypher(txt, fast)
                    done = True
                    break
                except Exception as e:
                    print(e)
                    options = [("retry", "*try again", ""),
                               ("menu", "or go back to *menu", "")]
                    answ = ui.get_choice("Could not convert that data into "
                                         "morse, please", options,
                                         oneline=True)
                    if answ in {None, "menu"}:
                        return

            if done:
                ui.text_output("Data successfully converted", txt,
                               "Morse form of data")

            options = [("redo", "*cypher another data", ""),
                       ("quit", "or go back to *menu", "")]
            answ = ui.get_choice("Do you want to", options, oneline=True)
            if answ in {None, "quit"}:
                return

    def decypher(self, ui):
        """Interactive version of decypher()."""
        txt = ""
        ui.message("===== Decypher Mode =====")

        while 1:
            txt = ui.text_input("Please choose some morse text")

            try:
                ui.text_output("Data successfully decypherd",
                               morse.decypher(txt),
                               "The hidden data is")
            except Exception as e:
                ui.message(str(e), ui.ERROR)

            options = [("redo", "*decypher another data", ""),
                       ("quit", "or go back to *menu", "")]
            answ = ui.get_choice("Do you want to", options, oneline=True)
            if answ == "quit":
                return


NAME = "*morse"
TIP = "Tool to convert text to/from morse code."
TYPE = app.cli.Node.TOOL
CLASS = Morse

# Allow tool to be used directly, without using Cyprium menu.
if __name__ == "__main__":
    import app.cli.ui
    ui = app.cli.ui.UI()
    tree = app.cli.NoTree("Morse")
    Morse(tree).main(ui)
