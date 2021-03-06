###############################################################################
# Copyright (c) 2006-2013 Franz Inc.
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Eclipse Public License v1.0
# which accompanies this distribution, and is available at
# http://www.eclipse.org/legal/epl-v10.html
###############################################################################

import urllib

def local(name, catalog=None):
  if catalog: return "<%s:%s>" % (catalog, name)
  else: return "<%s>" % name

def remote(name, catalog=None, host="localhost", port=10035, protocol="http"):
  if catalog: catalog = "/catalogs/" + urllib.quote(catalog)
  return "<%s://%s:%d%s/repositories/%s>" % (protocol, host, port, catalog or "", urllib.quote(name))

def url(url):
  return "<%s>" % url

def federate(*stores):
  return " + ".join(stores)

def reason(store, reasoner="rdfs++"):
  return "%s[%s]" % (store, reasoner)

def graphFilter(store, graphs):
  def asGraph(x):
    if x is None: return "null"
    else: return str(x)
  return "%s{%s}" % (store, " ".join(map(asGraph, graphs)))
