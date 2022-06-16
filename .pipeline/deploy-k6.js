'use strict';
const settings = require('./lib/config.js')
const task = require('./lib/deploy-k6.js')

task(Object.assign(settings, { phase: settings.options.env}));
