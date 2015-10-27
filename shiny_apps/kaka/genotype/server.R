library(shiny)
library(ggplot2)

choices <- c("crew", "fishob", "city") 


lappend <- function (lst, ...){
	lst <- c(lst, list(...))
	return(lst)
}


sanitise_header <-function(lst){
	lst <- gsub(" ",".", lst)
    lst <- gsub("/",".", lst)
	lst <- gsub("\\(",".", lst)
	lst <- gsub("\\)",".", lst)
	lst
}


get_seafood_headers <- function(selected){
	selected <- sanitise_header(selected)
    gs <- read.csv(paste('http://web:8000/report/experiment/csv/', sep=''), header=TRUE)
    gs <- unique(gs$group)
    gs <- sanitise_header(gs)
    selected <- selected[! selected %in% gs]
	selected
}

# Define server logic required to summarize and view the selected
# dataset

push_item <- function(prev, cur, nxt){
	
}

# returns string w/o leading whitespace
trim.leading <- function (x)  sub("^\\s+", "", x)

# returns string w/o trailing whitespace
trim.trailing <- function (x) sub("\\s+$", "", x)

# returns string w/o leading or trailing whitespace
trim <- function (x) gsub("^\\s+|\\s+$", "", x)


shinyServer(function(input, output, session) {

    # By declaring datasetInput as a reactive expression we ensure 
    # that:
    #
    #  1) It is only called when the inputs it depends on changes
    #  2) The computation and result are shared by all the callers 
    #       (it only executes a single time)
    #

	# Render teh data source tree

	output$datasource <- renderTree({
		dat <- read.csv(paste('http://web:8000/report/fish_datasource/csv/?ds_group=Seafood', sep=''), header=TRUE)
		suppliers <- levels(unique(dat[,"supplier"]))
		tr <- list()
		for(i in seq(length(suppliers))){
			tr[[suppliers[i]]] <- list()
		}
		for(i in seq(nrow(dat))){
			l <- trim(toString(paste(dat[i, "name"],"[",dat[i,"id"],"]", sep="")))
			s <- dat[i, "supplier"]
			tr[[s]][[l]] <- ""
		}
		tr
	})

	output$tree <- renderTree({
		dat <- read.csv(paste('http://web:8000/report/experiment/csv/', sep=''), header=TRUE)

		dat <- levels(unique(dat[,"name"])) 

		tr <- list()

		for(i in seq(length(dat))){
			tr[[dat[i]]] <- ""
        }
		tr
  	})
 
    datasetInput <- reactive({
        get_selected(input$tree)
        read.csv(paste('http://web:8000/report/genotype/csv/?term=QTL', sep=''), header=TRUE)
    }) 


	termInput <- reactive({
        read.csv(paste('http://web:8000/report/fish_term/csv/', sep=''), header=TRUE)
    })


	demoInput <- reactive({
        dat <- read.csv('http://web:8000/report/lengthfrequencyob/?fmt=csv/', header=TRUE)
		flt <- input$group
		if(flt == 'None'){
			dat <- data.frame(dat[c("length..mm.")])
			dat$cond <- 1
			names(dat) <- c('length', 'cond')
		}
		else{
			dat <- data.frame(dat[c(flt,"length..mm.")])	
			names(dat) <- c('cond', 'length')
		}
		dat
    })


    observe({
        x <- input$show_vars
        selected <- x
    })
  
    # The output$view depends on both the databaseInput reactive
    # expression and input$obs, so will be re-executed whenever
    # input$dataset or input$obs is changed. 
    output$seafoodview <- renderDataTable({
		#selected <- unlist(get_selected(input$tree))
		#selected <- get_seafood_headers(selected)
        ds <- datasetInput()
		ds.names = names(ds)
		sel <- intersect(selected,ds.names)
		ds
    })

	output$seafoodterms <- renderDataTable({
		termInput()
	})

	output$seafooddemo <- renderPlot({
		dat <- demoInput()
		ggplot(dat, aes(length, fill=cond)) + geom_histogram()
	})

    output$downloadData <- downloadHandler(
        filename = function() { 
                paste('fish.csv', sep='') 
        },
        content = function(file) {
			selected <- unlist(get_selected(input$tree))
			selected <- get_seafood_headers(selected)
			ds <- datasetInput()
	        ds.names = names(ds)
    	    sel <- intersect(selected,ds.names)
			sel <- c("fish", "trip", "tow",  sel)
            write.csv(ds[,sel], file)
        }
    )
})




