# -*- coding: utf-8 -*-

import tornado.web
import tornado.websocket
import tornado.httpserver
import tornado.ioloop
import sys

listeners = {}

class BaseHandler(tornado.web.RequestHandler):
  """
  Define encapsulate method to encapsulate datas
  """
  def encapsulate(self, success, data):
    if success:
      return {"success": True, "data": data}
    else:
      return {"success": False, "error": data}

  def answer(self, success, data):
    self.write(json.dumps(self.encapsulate(success, data)))

class IndexPageHandler(BaseHandler):
  def get(self):
    self.render("index.html")

class VersionHandler(BaseHandler):
  def get(self):
    response = {"name": "RESTinPy", "version": "0.3.1"}
    self.write(response)

"""
class WaveFlowHandler(tornado.websocket.WebSocketHandler):
  def check_origin(self, origin):
    return True

  def open(self):
    uid = self.get_secure_cookie("user")
    wid = self.get_secure_cookie("wave")

    if wid == None:
      self.close(code=403, reason="You are not connected to any Wave.")
      return

    if uid != None:
      success, user = UserManager.get_user(uid)
      firstname = user["firstName"]
    else:
      self.close(code=403, reason="You are not authenticated.")
      return

    try:
      listeners[str(wid)].append([uid, firstname, self])
    except:
      listeners[str(wid)] = [[uid, firstname, self]]

    #for [u_uid, u_fn, u_socket] in listeners[str(wid)]:


    self.write_message("Welcome " + firstname + " ! You're now connected.")

  def on_message(self, message):
    wid = self.get_secure_cookie("wave")
    uid = self.get_secure_cookie("user")

    for [user, firstname, socket] in listeners[str(wid)]:
      try:
        socket.write_message(firstname + ': ' + message)
      except WebSocketClosedError:
        listeners[str(wid)].remove([user, firstname, socket])
"""
