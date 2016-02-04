/**
 * Copyright 2014 IBM Corp. All Rights Reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

'use strict';

var proxyMiddleware = require('http-proxy-middleware'),
    extend = require('util')._extend;

/**
 * Proxy Middleware for Tradeoff Analytics.
 * Based on the 'http-proxy-middleware' node module.
 *
 * Accepts an options object with the following optional fields:
 *
 * - proxyPath - the root path for the proxy end-points (defaults to tradeof-analytics-proxy)
 * - sendIp - Boolean: add client IP to x-watson-metadata header? default - true
 *
 * The following fields may be obtained by looking at the service binding credentials in Bluemix.
 * This is useful for working outside of Bluemix (in developement or when running on an external server).
 * When working in Bluemix, the values will be overridden with those obtained from the VCAP_SERVICES environment variable.
 *
 * - url      - service url
 * - version  - service version
 * - username - service binding credentials
 * - password - service binding credentials
 *
 */
module.exports = function(options) {
  var defaultOptions = {
      url:"https://gateway.watsonplatform.net/tradeoff-analytics/api",
      version: 'v1',
      username: 'ba07d3ef-f18f-4bca-b421-4ffef88c359f',
      password: 'zxDuZj9aYwzm',
      proxyPath: '/tradeoff-analytics-proxy',
      sendIp: true
  };
  options = extend(defaultOptions, options);  // override defaults
  //obtain credentials from bluemix environment variable VCAP_SERVICES
  options = extend(options, getServiceCreds('tradeoff_analytics'));
  var pathRewrite = {};
  pathRewrite['^' + options.proxyPath +'/dilemmas'] = '/dilemmas';
  pathRewrite['^' + options.proxyPath +'/events'] = '/events';

  var proxyOptions = {
    target: options.url +'/' + options.version,
    auth: options.username+':'+options.password,
    pathRewrite: pathRewrite,
    onError: function (err, req, res) {
      res.writeHead(502, {
        'Content-Type': 'text/plain'
      });
      res.end('Error connecting to Watson Tradeoff Analytics');
    }
  };

  if (options.sendIp) {
    proxyOptions.onProxyReq= function(proxyReq, req, res) {
      // add ip address if client sent metadata
      var metadata = req.header('x-watson-metadata');
      if (metadata) {
        metadata += "client-ip:" + req.ip;
        proxyReq.setHeader('x-watson-metadata', metadata);
      }
    }
  }

  //Create the service wrapper
  return proxyMiddleware(options.proxyPath, proxyOptions);
}


/**
 * if VCAP_SERVICES exists then it returns username, password and url
 * for the first service that stars with 'name' or {} otherwise
 * @param  String name, service name
 * @return {Object} the service credentials or {} if
 * name is not found in VCAP_SERVICES
 */
function getServiceCreds(name) {
    if (process.env.VCAP_SERVICES) {
      var services = JSON.parse(process.env.VCAP_SERVICES);
      for (var service_name in services) {
          if (service_name.indexOf(name) === 0) {
              var service = services[service_name][0];
              return {
                  url: service.credentials.url,
                  username: service.credentials.username,
                  password: service.credentials.password
              };
          }
      }
    }
    return {};
};
