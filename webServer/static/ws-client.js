$(document).ready(function(){

        var WEBSOCKET_ROUTE = "/ws";

        if(window.location.protocol == "http:"){
            //localhost
            var ws = new WebSocket("ws://" + window.location.host + WEBSOCKET_ROUTE);
        }
        else if(window.location.protocol == "https:"){
            //Dataplicity
            var ws = new WebSocket("wss://" + window.location.host + WEBSOCKET_ROUTE);
        }

        ws.onopen = function(evt) {
            // $("#ws-status").html("Connected");
            // $("#ws-status").css("background-color", "#afa");
            // $("#server_light").val("ON");
            $("#signal").html("READY");
            $("#ws-status").html("Connected");
            $("#ws-status").css("background-color", "#afa");
        };

        ws.onmessage = function(evt) {
            //console.log(evt);
            var sData = JSON.parse(evt.data);
            //console.log(sData);
            if (sData.sensor !== 'undefined'){
              //console.log(sData.info + "|" + )

              if (sData.info == 'hello'){
                r = sData.reply.toString();
                $("#HelloResponse").html(r);
              }

              //WHAT TO DO WHEN WE GET A MESSAGE FROM THE SERVER
              if (sData.info == 'timer'){
                m = sData.m.toString();
                s = sData.s.toString().padStart(2,"0");
                $("#timeLeft").html(m + ":" + s);
              }

              // DISTANCE SENSOR (1/2)

              // measure once (button press)
              if (sData.info == 'S-one'){
                $("#sensor_measure").html(sData.S + ' ' + sData.units);
                let now = new Date();
                $("#sensor_time").html(now.toString().split(" GMT")[0]);
              }

              // write all data to log at end of sensing
              // if (sData.info == 'logT'){
              //   dataT.writeAllData(sData);
              // }
              //
              // // continuous log: Add one data point to graph and table
              // if (sData.info == 'logUp'){
              //   dataT.addRow(sData);
              //   graphT.addDataPoint(sData);
              //
              //   $("#countdownData").html("-"+sData.timeLeft+" s");
              //   $("#timeLeftT").css("width", 100*sData.timeLeft/timeLog+"%");
              // }
              //DISTANCE SENSOR (END)


            };
        };

        ws.onclose = function(evt) {
            $("#ws-status").html("Disconnected");
            $("#ws-status").css("background-color", "#faa");
            $("#server_light").val("OFF");
        };

        //MESSAGES TO SEND TO THE SERVER

        // DISTANCE SENSOR (2/2)

        $("#checkSensor").click(function(){
            let msg = '{"what": "checkS"}';
            ws.send(msg);
            let return_signal = "Checking " + this.value.split(" ")[1];
            $("#sensor_measure").html(return_signal);
        });

        $("#monitorSensor").click(function(){
          let dt = $("#monitorSec").val();
          let msg = {
            "what": "monitor",
            "dt": dt
          };
          ws.send(JSON.stringify(msg));
        })

        // $("#logT").click(function(){
        //     dataT = new dataTable("logData", "°C");
        //     dataT.setupTable();
        //
        //     graphT = new dataGraph("logGraph", "°C");
        //     $("#logGraph").css("height", "400px");
        //     console.log(graphT.plot.data);
        //
        //     let timeMin = parseInt($("#logT_timeMin").val());
        //     let timeSec = parseInt($("#logT_timeSec").val());
        //     timeLog = timeMin * 60 + timeSec;
        //
        //     let dtMin = parseInt($("#logT_dtMin").val());
        //     let dtSec = parseInt($("#logT_dtSec").val());
        //     let dt = dtMin * 60 + dtSec;
        //
        //     let msg = {
        //       "what": "logT",
        //       "t": timeLog,
        //       "dt": dt,
        //       "update": "live"
        //     }
        //     ws.send(JSON.stringify(msg));
        // });

        // DISTANCE SENSOR (END)


        $("#hello").click(function(){
            let msg = '{"what": "hello"}';
            ws.send(msg);
        });

        $("#timer").click(function(){
            let m = $("#timerMin").val();
            let s = $("#timerSec").val();
            let msg = '{"what": "timer", "minutes":'+ m + ', "seconds": '+ s + '}';
            ws.send(msg);
        });

        $("#reboot").click(function(){
            let check = confirm("Reboot Pi?");
            if (check){
              var msg = '{"what": "reboot"}';
              ws.send(msg);
            }
        });



      });
