library(rvest)
library(placement)

scrape_mystore411 = function(id, store_name, page_state, topProv = NA, secProv = NA, key){
    store_name = gsub(' ', '-', store_name)
    prov_home_url = paste('http://mystore411.com/store/list_state/', id, '/', sep = '')
    city_home_url = paste('http://mystore411.com/store/list_city/', id, '/', sep = '')
    end = paste('/Canada/', store_name, '-store-locations', sep = '')

    name = NULL
    address = NULL
    city = NULL
    prov = NULL
    postal = NULL
    lat = NULL
    lng = NULL

    if(page_state == 'top'){
        for(i in 1:length(topProv)){
            prov_url = paste(prov_home_url, topProv[i], end, sep = '')
            con = url(prov_url, 'rb')
            prov_store = read_html(con)
            prov_store_list = html_text(html_nodes(prov_store, 'td'))

            for(j in 1:length(prov_store_list)){
                city_url = paste(city_home_url, topProv[i], '/', prov_store_list[j], end, sep = '')
                city_url = gsub(" ", "%20", city_url)
                con = url(city_url, 'rb')
                city_store = read_html(con)
                city_store_list = unlist(html_nodes(city_store, 'a') %>% html_attr("href"))
                city_store_list = city_store_list[grepl('view', city_store_list)]
                
                if(length(city_store_list) == 0)
                    next
                
                for(k in 1:length(city_store_list)){
                    store_url = paste('http://mystore411.com', city_store_list[k], sep='')
                    con = url(store_url, 'rb')
                    store = read_html(con)
                    store_parsed = html_text(html_nodes(store, 'span'))
                    name = c(name, store_parsed[8])
                    address = c(address, store_parsed[10])
                    city = c(city, store_parsed[11])
                    prov = c(prov, store_parsed[12])
                    postal = c(postal, store_parsed[13])
                    add = paste(store_parsed[10], store_parsed[11], store_parsed[12], 'Canada', 
                        store_parsed[13])
                    coordset <- geocode_url(add, auth = "standard_api", privkey = geo_key, 
                        clean = TRUE, add_date = 'today', verbose = F)
                    lat = c(lat, coordset[1])
                    lng = c(lng, coordset[2])
                    print(store_parsed[8])
                    Sys.sleep(5)        
                }
            }
        }

        for(i in 1:length(secProv)){
            prov_url = paste(prov_home_url, secProv[i], end, sep = '')
            con = url(prov_url, 'rb')
            prov_store = read_html(con)
            prov_store_list = unlist(html_nodes(prov_store, 'a') %>% html_attr("href"))
            prov_store_list = prov_store_list[grepl('view', prov_store_list)]
            if(length(prov_store_list) == 0)
                next
            else{
                for(k in 1:length(prov_store_list)){
                    store_url = paste('http://mystore411.com', prov_store_list[k], sep='')
                    con = url(store_url, 'rb')
                    store = read_html(con)
                    store_parsed = html_text(html_nodes(store, 'span'))
                    name = c(name, store_parsed[8])
                    address = c(address, store_parsed[10])
                    city = c(city, store_parsed[11])
                    prov = c(prov, store_parsed[12])
                    postal = c(postal, store_parsed[13])
                    add = paste(store_parsed[10], store_parsed[11], store_parsed[12], 'Canada', 
                        store_parsed[13])
                    coordset <- geocode_url(add, auth = "standard_api", privkey = geo_key, 
                        clean = TRUE, add_date = 'today', verbose = F)
                    lat = c(lat, coordset[1])
                    lng = c(lng, coordset[2])
                    print(store_parsed[8])
                    Sys.sleep(5)        
                    }
            }
        }
    }

    if(page_state == 'single'){
        url = paste('http://www.mystore411.com/store/listing/', id, '/Canada/', store_name,
            '-store-locations', sep = '')
        store = read_html(url)
        store_list = unlist(html_nodes(store, 'a') %>% html_attr("href"))
        store_list = store_list[grepl('view', store_list)]
        for(k in 1:length(store_list)){
            store_url = paste('http://mystore411.com', store_list[k], sep='')
            store = read_html(store_url)
            store_parsed = html_text(html_nodes(store, 'span'))
            name = c(name, store_parsed[8])
            address = c(address, store_parsed[10])
            city = c(city, store_parsed[11])
            prov = c(prov, store_parsed[12])
            postal = c(postal, store_parsed[13])
            add = paste(store_parsed[10], store_parsed[11], store_parsed[12], 'Canada', 
                store_parsed[13])
            coordset <- geocode_url(add, auth="standard_api", privkey=key, clean=TRUE, add_date='today', verbose=F)
            lat = c(lat, coordset[1])
            lng = c(lng, coordset[2])
            print(store_parsed[8])
            Sys.sleep(5)        
        }
    }
    address = gsub('\r\n         ', '', address)
    export = cbind(name, address, city, prov, postal, unlist(lat), unlist(lng))
    export = export[!duplicated(export), ]
    # write.table(export, paste('C:/Users/Zheng/Downloads/', store_name, '.txt', sep = ''), 
    #     sep = "\t", row.names = F)
    return(export)
}