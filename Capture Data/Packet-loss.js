const Monitor = require('ping-monitor');
 
const myMonitor = new Monitor(
    {
        address: '8.8.8.8',
        port: '53',
        title: 'Google DNS',
        interval: 500,

        config: {
            intervalUnits: 'milliseconds' // seconds, milliseconds, minutes {default}, hours
          },
        expect: {
            statusCode: 200
        }
    }
);

myMonitor.on('up', function (res, state) {
    console.log({"Time" : state.lastRequest, "State" : 200 , "responseTime" : res.responseTime});
});


myMonitor.on('down', function (res) {
    console.log({"Time" : myMonitor.lastDownTime, "State" : -1 , "responseTime" : res.responseTime});
});


myMonitor.on('stop', function (website) {
    console.log(website);
});

myMonitor.on('error', function (error) {
    console.log({"Time" : myMonitor.lastDownTime, "State" : -2 , "responseTime" : -1});
});

setInterval(() => {
    
    console.log({'totalRequests' : myMonitor.totalRequests, 'totalDownTimes' : myMonitor.totalDownTimes, 'PercDown' : Math.round((myMonitor.totalDownTimes/myMonitor.totalRequests) * 100)});
    }, 60000);