-- configuration
SSID = "<INSERT SSID HERE>"
KEY  = "<INSERT WIFI KEY HERE>"
HOST = "danielrojas.net"
URL  = "http://danielrojas.net/iot/traintimes/bvg.php"

function fetchdata()
    conn=net.createConnection(net.TCP, 0)
    conn:on("receive",
    function(conn, payload)
        datastart = string.find(payload, "{")
        dataend   = string.find(payload, "}")
        if datastart ~= nil and dataend ~= nil then
            data      = string.sub (payload, datastart, dataend)
            for i in string.gmatch(data, "%C+") do -- split lines
                print(i)
            end
        else
            --invalid data
        end
    end )
    conn:on("connection",
    function(c)
        conn:send("GET " .. URL .. " HTTP/1.1\r\nHost: " .. HOST .. "\r\n"
            .."Connection: keep-alive\r\nAccept: */*\r\n\r\n")
    end)
    conn:on("disconnection",
    function(c)
        --print ("disconnected")
    end)
    conn:connect(80,HOST)
end

wifi.setmode(wifi.STATION)
wifi.sta.config(SSID,KEY)
wifi.sta.connect()

fetchdata()

tmr.alarm(0, 60000, 1, fetchdata)
