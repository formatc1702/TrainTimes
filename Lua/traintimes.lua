-- configuration
-- TODO : point the following four lines to usersettings.lua
-- SSID = "<INSERT SSID HERE>"
-- KEY  = "<INSERT WIFI KEY HERE>"
-- HOST = "danielrojas.net"
-- URL  = "http://danielrojas.net/iot/traintimes/bvg.php"

active = 0

function fetchdata()
    if active == 0 then
        active = 1
        wifi.setmode(wifi.STATION)
        wifi.sta.config(SSID,KEY)
        wifi.sta.connect()
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
            conn:close()
        end )
        conn:on("connection",
        function(c)
            conn:send("GET " .. URL .. " HTTP/1.1\r\nHost: " .. HOST .. "\r\n"
                .."Accept: */*\r\n\r\n")
            -- conn:send("GET " .. URL .. " HTTP/1.1\r\nHost: " .. HOST .. "\r\n"
                -- .."Connection: keep-alive\r\nAccept: */*\r\n\r\n")
        end)
        conn:on("disconnection",
        function(c)
            wifi.sta.disconnect()
            active = 0
            -- print ("disconnected")
        end)
        conn:connect(80,HOST)
    end
end

fetchdata()

uart.on("data", 0, function(data)
    if     data=="!" then
        -- print("Once")
        fetchdata()
    elseif data=="1" then
        -- print("Repeat")
        fetchdata()
        tmr.alarm(0, 60000, 1, function()
            fetchdata()
            end)
    elseif data=="0" then
        -- print("Stop")
        tmr.stop(0)
    end
    end, 0)
