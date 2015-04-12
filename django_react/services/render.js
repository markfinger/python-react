var reactRender = require('react-render');

module.exports = function(data, res) {
  reactRender(data, function(err, markup) {
    if (err) return res.status(500).end(err.stack);

    res.end(markup);
  });
};