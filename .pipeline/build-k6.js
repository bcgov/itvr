'use strict';
const task = require('./lib/build-k6.js')
const settings = require('./lib/config.js')

task(Object.assign(settings, { phase: 'build'}))
