const baseConfig = require('./jest.config.cjs');

/** @type {import('jest').Config} */
module.exports = {
  ...baseConfig,
  testMatch: ['**/__a11y__/**/*.test.(ts|tsx)'],
};
