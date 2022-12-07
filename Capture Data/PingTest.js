var ping = require ("net-ping");

function pingTargets(target, callback, date)
{
 
    var options = {
        retries: 3,
        timeout: 2000,
        packetSize: 128
    };
    
    var session = ping.createSession (options);
    
    session.on ("error", function (error) {
        console.trace (error.toString ());
    });
    
    
    session.pingHost (target, function (error, retTarget, sent, rcvd) {
        var ms = rcvd - sent;
        if (error)
            if (error instanceof ping.RequestTimedOutError)
            {
                callback (0, -1, date);
            }
            else
            {
                callback (-1, error.toString(), date);
            }
        else
        {
            callback (1 , ms, date);
        }
    });
}

exports.pingTargets = pingTargets;