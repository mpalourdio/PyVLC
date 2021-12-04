# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import sys
from datetime import datetime

import vlc
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget, QPushButton


class MyPlayer:
    def __init__(self):
        # List of songs You should fetch from your collection. Hard coded list for convenience
        # Replace this by your own files, located in the same directory as test.py to test
        self.songs = ["tmp/1.mp3", "tmp/2.mp3"]

        # First song of the list, ok layzzz gooooo
        self.currentSongIndex = 0

        # Build app layout
        self.app = QApplication(sys.argv)
        self.window = QWidget()
        self.window.setWindowTitle("PyVLC")
        self.vbox = QVBoxLayout()
        self.vbox.addStretch()
        self.l1 = QLabel()
        self.vbox.addWidget(self.l1)
        self.l2 = QLabel()
        self.vbox.addWidget(self.l2)
        self.l3 = QLabel()
        self.vbox.addWidget(self.l3)

        self.button1 = QPushButton()
        self.button1.setText("Button1")
        self.vbox.addWidget(self.button1)
        self.button1.clicked.connect(self.__buttonClicked)



        self.window.setLayout(self.vbox)
        self.window.show()

    def playSong(self, song):
        self.title = self.songs[self.currentSongIndex]

        # This is a singleton, no worry in fetching it all the time
        player = vlc.MediaPlayer()
        player.set_media(vlc.Media(song))
        player.play()

        events = player.event_manager()
        events.event_attach(vlc.EventType.MediaPlayerEndReached, self.__playNextSong)
        events.event_attach(vlc.EventType.MediaPlayerTimeChanged, self.__trackTime, player)

    def __playNextSong(self, event):
        # Next song we want to play is the next item in the list, hey!
        self.currentSongIndex += 1

        # Once the end of the list is reached, we do not play songs anymore, or we'll be out-of-bound
        if self.currentSongIndex < len(self.songs):
            self.playSong(self.songs[self.currentSongIndex])

    def __trackTime(self, event, player):
        self.l1.setText(self.title + " -> " + str(player.get_time() / 1000) + " s")
        self.l2.setText(str(player.get_position()))

    def __buttonClicked (self):
        self.l3.setText("Clicked at :" + datetime.now().strftime("%H:%M:%S"))



myPlayer = MyPlayer()
myPlayer.playSong(myPlayer.songs[myPlayer.currentSongIndex])

sys.exit(myPlayer.app.exec_())
