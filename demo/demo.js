var dj = require('./djangode');
var sys = require('sys')

var sqlite = require('sqlite')
var db = new sqlite.Database();
db.open('vizdata.sqlite3', function() {
    db.execute("select load_extension('libspatialite.2.dylib')", function(error, rows) {
        if (error) {
            sys.log(error);
        } else {
            sys.log(JSON.stringify(rows))
        }
    })
})

var app = dj.makeApp([
    ['^/$', function(req, res) {
        dj.serveFile(req, res, 'static/index.html');
    }],
    ['^/(static/.*)$', dj.serveFile],
    ['^/pol/(\\d+)/contributions', function(req, res, id) {
        db.execute('select x, y from contributions where pols_id = ? and x is not null and y is not null', [id], function(error, rows) {
            if (error) {
                sys.log(error);
            } else {
                dj.respond(res, JSON.stringify(rows))
            }
        })
    }]
]);

dj.serve(app, 8009);
