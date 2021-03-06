import signal, os
import thread
import gi

gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')

from PokemonGoClient import get_pokengo_server_status
from gi.repository import Gtk as gtk
from gi.repository import AppIndicator3 as appindicator
from gi.repository import GObject as gobject

BASE_PATH = os.path.dirname(os.path.realpath(__file__))
POKE_ONLINE = BASE_PATH + '/icons/w/pokeok.png'
POKE_OFFLINE = BASE_PATH + '/icons/w/pokedown.png'
POKE_UNSTABLE = BASE_PATH + '/icons/w/pokeunstable.png'


class PokemonGoIndicator:
	APPINDICATOR_ID = 'myappindicator'
	indicator = None
	icon = POKE_OFFLINE

	def __init__(self, indicator_id='myappindicator'):
		self.APPINDICATOR_ID = indicator_id

		self.indicator = appindicator.Indicator.new( self.APPINDICATOR_ID, 'whatever', appindicator.IndicatorCategory.SYSTEM_SERVICES)
		self.indicator.set_status(appindicator.IndicatorStatus.ACTIVE)

		# Set Menu
		menu = gtk.Menu()

		item_quit = gtk.MenuItem('Quit')
		item_quit.connect('activate', self.quit)

		menu.show_all()

		self.indicator.set_menu( menu )


		self.update_server_status_icon()

		signal.signal( signal.SIGINT, signal.SIG_DFL )

		gtk.main()

	def set_icon(self, icon_path):
		self.icon = os.path.dirname(os.path.realpath(__file__)) + '/' + icon_path

	def get_icon(self):
		print self.icon
		return self.icon

	def quit(self, source):
		gtk.main_quit()

	def update_server_status_icon(self):
		status = get_pokengo_server_status()

		ICONS = {
			"Online!": POKE_ONLINE,
			"Unstable!": POKE_UNSTABLE,
			"Offline!": POKE_OFFLINE
		}

		self.indicator.set_icon( ICONS[status] )
		gobject.timeout_add_seconds( 60, self.update_server_status_icon )

if __name__ == '__main__':
	ap = PokemonGoIndicator('pokemongoindicator')
