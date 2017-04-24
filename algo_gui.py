import gtk
import proj
class GUI:
	def destroy(self,Widget):
		gtk.main_quit()
	'''
	def on_info(self, widget):
		md = gtk.MessageDialog(self,gtk.DIALOG_DESTROY_WITH_PARENT,gtk.MESSAGE_INFO,gtk.BUTTONS_CLOSE,"Download completed")
        md.run()
        md.destroy()
    '''

	def Find(self,button,entry,label2):
		input = entry.get_text()
		pred = proj.inpt(input)
		label2.set_markup(pred)
		

	def __init__(self):
		window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		window.set_title("Enter Message")
		window.set_policy(True, True, False)
		window.connect("destroy",self.destroy)
		window.set_default_size(400,150)
		window.set_border_width(0)

		box1 = gtk.VBox(True,0)
		window.add(box1)
		box1.show()

		label1 = gtk.Label("Enter the message :")
		box1.pack_start(label1,False,False,0)
		label1.show()

		entry=gtk.Entry()
		box1.pack_start(entry,True,True,0)
		entry.show()

		table= gtk.Table(1,3,True)
		box1.pack_start(table,False,False,0)
		table.show()

		label2=gtk.Label()
		but=gtk.Button("Find!")
		table.attach(but,4,5,0,1,gtk.FILL,gtk.FILL,0,0)
		but.connect("clicked",self.Find,entry,label2)
		but.show()

		
		box1.pack_start(label2,False,False,0)
		label2.show()

		window.show()

	def main(self):
		gtk.main()

if __name__=='__main__':
	disp = GUI()
	disp.main()