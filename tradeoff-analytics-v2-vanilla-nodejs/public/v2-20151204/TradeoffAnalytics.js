/*******************************************************************************
 * IBM Confidential
 *
 * Licensed Materials - Property of IBM
 *
 * AUS720150196
 *  Â© Copyright IBM Corp. 2015 All Rights Reserved
 *
 * US Government Users Restricted Rights - Use, duplication or disclosure
 * restricted by GSA ADP Schedule Contract with IBM Corp.
 ******************************************************************************/

"use strict";

(function(){
  window.TA = {};
  var wasEverStarted = false;
  TA.TradeoffAnalytics = function(ops /*object*/, node /*string or object*/) {//constructor

    assert(ops, 'options argument was not provided');
    assert(typeof (ops.dilemmaServiceUrl) === 'string',
        "Invalid \'dilemmaServiceUrl\' parameter. Expected value of type string.");
    assert((!ops.customCssUrl) || typeof (ops.customCssUrl) === 'string',
        "Invalid \'customCssUrl\' parameter. Expected value of type string.");
    assert((!ops.errCallback) || typeof (ops.errCallback) === 'function',
        "Invalid \'errCallback\' parameter. Expected value of type function.");
    assert((!ops.username) || typeof (ops.username) === 'string',
        "Invalid \'username\' parameter. Expected value of type string.");
    assert((!ops.password) || typeof (ops.password) === 'string',
        "Invalid \'password\' parameter. Expected value of type string.");
    assert((!ops.locale) || typeof (ops.locale) === 'string',
        "Invalid \'locale\' parameter. Expected value of type string.");

    ops.dev = ops.dev || getQueryVariable('dev')==='true';
    ops.locale = ops.locale || getQueryVariable('locale');

    this.node = typeof (node) === 'string' ? document.getElementById(node) : node;
    assert(this.node, 'Container node was not provided.');

    this.topics = {
        started :[],
        afterError : [],
        problemChanged :[],
        optionClicked : [],
        doneClicked : [],
        destroyed : [],
        X_favoritesChanged : [],
        X_selectionChanged : [],
        X_finalDecisionChanged : [],
        X_filterChanged : [],
        X_optionHovered : []
      };
      this.subscribe = function(topic /*string*/, callback /*function*/) {
        assert(this.topics[topic] instanceof Array, "unknown topic '"+topic+"'");
        assert(typeof (callback) === 'function', 'callback must be a function');
        assert(this.topics[topic].indexOf(callback) === -1, 'callback already registred');
        this.topics[topic].push(callback);
        var self = topic;
        return {
          unsubscribe : function(){
            this.clearSubscription(topic, callback)
          }.bind(this)
        };
      };
      this.publish = function(topic /*string*/, payload /*object*/) {
        var arr = this.topics[topic];
        assert(arr instanceof Array);
        for (var i = 0; i < arr.length; i++) {
          arr[i].apply(undefined, [payload]);
        }
      };
      this.clearAllSubscriptions = function() {
        for ( var topic in this.topics) {
          this.clearSubscriptions(topic);
        }
      };
      this.clearSubscriptions = function(topic /*string*/) {
        for (var i = 0; i < this.topics[topic].length; i++) {
          this.clearSubscription(topic, this.topics[topic][i]);
        }
      };

      this.node = typeof (node) === 'string' ? document.getElementById(node) : node;
      this.state = 'created';

      this.start = function(startedCallback) {
        assert(this.state === 'created', 'TradeoffAnalytics widget cannot be started!');
        var taLibRoot = getTaLibRoot();

        this.state = 'starting';

        var iframeInitialized = function() {
          var msg = {
            type : 'start',
            content : {
              taLibRoot : taLibRoot,
              devMode : ops.dev,
              customCssUrl : ops.customCssUrl,
              profile : ops.profile,
              locale : ops.locale,
              metadata: ops.metadata
            }
          };
          var fn = function(event){
            if(event.data.type ==='started'){
              this._removeEventListener (fn);
              this.state = 'started';
              startedCallback && startedCallback(event.data.content);
            }
          }.bind(this);
          this._addEventListener (fn);
          this._postMessageToIframe(msg);
        }.bind(this);

        var iframeLoaded = function() {
          var fn = function(event){
            if(event.data ==='ta_initialized'){
              this._removeEventListener (fn);
              this.state = 'initialized';
              iframeInitialized();
            }
          }.bind(this);
          this._addEventListener (fn);
        }.bind(this);

        this.iframe = createDom('iframe', {
          src : taLibRoot + 'TradeoffAnalyticsIframe.html',
          onload : iframeLoaded
        }, this.node);
        this.iframe.style.border = 0;
        this.iframe.style.height = '100%';
        this.iframe.style.width = '100%';

        this._addEventListener( this._receiveMessage);
      };

      this._addEventListener = function(listener){
        if (window.addEventListener) {
          window.addEventListener('message', listener, false);
        } else {
          window.attachEvent('onmessage', listener);
        }
      };

      this._removeEventListener = function(listener){
        if (window.removeEventListener) {
          window.removeEventListener('message', listener, false);
        } else {
          window.detachEvent('onmessage', listener);
        }
      };

      this.show = function(problem, showingCallback, metadata) {
        assert(this.state === 'started', 'TradeoffAnalytics was not started');
        assert(typeof (showingCallback) === 'undefined' || typeof (showingCallback) === 'function',  "\'showingCallback\' is not a function");
        var msg = {
          type : 'show',
          content : {
            problem : problem,
            metadata: typeof (metadata) === 'object' ? metadata : undefined
          }
        };
        this._postMessageToIframe(msg);
        if(showingCallback){
          var fn = function(event){
            if(event.data.type ==='showing'){
              showingCallback(event.data.content);
              this._removeEventListener (fn);
            }
          }.bind(this);
          this._addEventListener (fn);
        }

        if (typeof (metadata) === 'function') {   // backward compatibility with beta, where 3rd param was the callback for doneClicked
        	this.subscribe('doneClicked', metadata);
        }

      };

      this.resize = function(width /*number*/, height /*number*/) {
        assert(this.state === 'started', 'TradeoffAnalytics was not started');
        assert(typeof (width) === 'undefined' || typeof (width) === 'number',
            "\'width\' provided but it is not a number (of pixels)");
        assert(typeof (height) === 'undefined' || typeof (height) === 'number',
            "\'height\' provided but it is not a number (of pixels)");

        this.iframe.style.width = width ? '' + width + 'px' : '100%';
        this.iframe.style.height = height ? '' + height + 'px' : '100%';
      };

      this.destroy = function(destroyedCallback /*function*/) {
        assert(this.state === 'started', 'TradeoffAnalytics was not started');
        assert(typeof (destroyedCallback) === 'undefined' || typeof (destroyedCallback) === 'function',  "\'destroyedCallback\' is not a function");

        this._postMessageToIframe({
          type : 'destroy'
        });
        var fn = function(event){
          if(event.data.type ==='destroyed'){
            this._removeEventListener (fn);
            this._removeEventListener(this._receiveMessage);
            this.node.removeChild(this.iframe);
            this.state = 'destroyed';
            destroyedCallback && destroyedCallback(event.data.content);
          }
        }.bind(this);
        this._addEventListener (fn);
      };

      this._postMessageToIframe = function(msg) {
        if (this.iframe.contentWindow) {
  	      this.iframe.contentWindow.postMessage(msg, '*');
        }

      };

      this.importantEvents = [ 'started', 'dilemma', 'afterShow', 'problemChanged', 'afterDone', 'destroyed', 'afterError','analyticsEvents'];
      this.notificationEvents = ['optionClicked', 'X_finalDecisionChanged', 'X_favoritesChanged','X_selectionChanged', 'doneClicked', 'X_filterChanged', 'X_optionHovered' ];

      this._receiveMessage = function(event) {
        if (this.importantEvents.indexOf(event.data.type) < 0 && this.notificationEvents.indexOf(event.data.type) < 0) {
          return;
        }
        switch (event.data.type) {
        case 'dilemma':
          var reqNum = event.data.content.reqNum,
            _this = this;
          (function() {
            var problem = event.data.content.problem;
            var headers = event.data.content.headers || {};
            headers['Content-Type'] = 'application/json; charset=utf-8';

            var url = ops.dilemmaServiceUrl + (event.data.content.changeUrlSuffix || '');
            var okCallback = function(response) {
              var respObj = JSON.parse(response);
              this._postMessageToIframe({
                type : 'afterDilemma',
                reqNum : reqNum,
                content : respObj
              });
            }.bind(this);
            var errCallback = function(err) {
              this._postMessageToIframe({
                type : 'afterDilemmaError',
                reqNum : reqNum,
                content : {
                  err : err
                }
              });
            }.bind(this);

            xhr(url, 'POST', headers, JSON.stringify(problem), okCallback, errCallback, ops.username, ops.password);
          }.bind(this)());

          break;
        case 'analyticsEvents':
          (function() {
            var reqNum = event.data.content.reqNum;
            var events = event.data.content.events;
            var url = ops.analyticsEventsUrl;

            var okCallback = function(response) {
              this._postMessageToIframe({
                type : 'afterAnalyticsEvents',
                reqNum: reqNum
              });
            }.bind(this);
            var errCallback = function(err) {
              this._postMessageToIframe({
                type : 'afterAnalyticsEventsError',
                reqNum : reqNum,
                content : {
                  err : err
                }
              });
            }.bind(this);
            var headers = event.data.headers;
            headers['Content-Type'] = 'application/json; charset=utf-8';

            if (url) {
  	          xhr(url, 'POST', headers, events, okCallback, errCallback, ops.username, ops.password);
            }
            else {
          	  okCallback();
            }
          }.bind(this)());
        break;

        case 'afterError':
          var obj = event.data.content || {};
          ops.errCallback && ops.errCallback(obj);
          break;
        default:
          // console.info('ignored');
        }

        if(this.topics[event.data.type] instanceof Array){
          var obj = event.data.content || {};
          obj.type = event.data.type;
          this.publish(event.data.type, obj);
        }
      }.bind(this);
  };

  // UTILITIES
  function getQueryVariable(variable){
    var query = window.location.search.substring(1);
    var vars = query.split("&");
    for (var i=0;i<vars.length;i++) {
      var pair = vars[i].split("=");
      if(pair[0] == variable){
        return pair[1];}
      }
      return undefined;
  }
  function getTaLibRoot() {
    for (var i = 0; i < document.scripts.length; i++) {
      var src = document.scripts[i].src;
      var index = src.indexOf('TradeoffAnalytics.js');
      if (index >= 0) {
        return src.substring(0, index);
      }
    }
  };

  function createDom(elem, map, parent) {
    var e = document.createElement(elem);
    for ( var k in map) {
      e[k] = map[k];
    }
    parent.appendChild(e);
    return e;
  };
  function assert(cond, message) {
    if (!cond) {
      throw message;
    }
  };

  function xhr(url, method, headers, body, okCallback, errCallback, username, password) {
    [ okCallback, errCallback ].forEach(function(f) {
      if (typeof (f) != 'function') {
        throw 'invalid callback function';
      }
    });
    var xmlhttp = new XMLHttpRequest();
    // xmlhttp.onload = okCallback;
    // xmlhttp.onerror = errCallback;
    xmlhttp.onreadystatechange = function() {
      if (xmlhttp.readyState === 4) {
        if (xmlhttp.status === 200) {
          okCallback(xmlhttp.responseText);
        } else {
          var err = {
            message : xmlhttp.statusText || 'Connection error',
            responseText : xmlhttp.responseText,
            status : xmlhttp.status
          };
          errCallback(err);
        }
      }
    };
    xmlhttp.open(method, url, true, username, password);
    for ( var att in headers) {
      xmlhttp.setRequestHeader(att, headers[att]);
    }

    xmlhttp.send(body);
  };

})();
