library(shiny)
library(ggplot2)
library(rkaka)


choices <- c("crew", "fishob", "city") 


lappend <- function (lst, ...){
	lst <- c(lst, list(...))
	return(lst)
}


sanitise_header <-function(lst){
	lst <- gsub(" ","_", lst)
    lst <- gsub("/","_", lst)
	lst <- gsub("\\(","_", lst)
	lst <- gsub("\\)","_", lst)
	lst
}


get_seafood_headers <- function(selected){
	selected <- sanitise_header(selected)
    gs <- kaka.qry("tree","")
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
        dat <- kaka.qry("data_source", "")
        tr <- list()
        tr[["test"]] <- list() 
		for(i in seq(nrow(dat))){
			l <- trim(toString(dat[i, "name"]))
			tr[["test"]][[l]] <- ""
		}
		tr
	})

	output$tree <- renderTree({
        dat <- kaka.qry("tree","")

		dat <- dat[order(dat$Level_1,dat$Level_2,dat$Level_3,dat$Level_4,dat$Level_5),]

		tr <- list()

		for(i in seq(nrow(dat))){
			l1 <- trim(toString(dat[i, "Level_1"]))
		  	l2 <- trim(toString(dat[i, "Level_2"]))
		  	l3 <- trim(toString(dat[i, "Level_3"]))
		  	l4 <- trim(toString(dat[i, "Level_4"]))
		  	l5 <- trim(toString(dat[i, "Level_5"]))
		
			#print(paste(i,l1,l2,l3,l4,l5, sep="/"))
			if(l2 == "" | is.null(l2)){
				tr[[l1]] <- ""
			}
			else{
				if(l3 == "" | is.null(l3)){
					tr[[l1]][[l2]] <- ""
				}
				else{
					if(l4 == "" | is.null(l4)){
						if(!is.list(tr[[l1]][[l2]])){
							tr[[l1]][[l2]] = list()
						}
						tr[[l1]][[l2]][[l3]] <- ""
					}
					else{
						if(l5 == "" | is.null(l5)){
							if(!is.list(tr[[l1]][[l2]][[l3]])){
		                        tr[[l1]][[l2]][[l3]] = list()
    		                }
                        	tr[[l1]][[l2]][[l3]][[l4]] <- ""
                       	}
						else{
							if(!is.list(tr[[l1]][[l2]][[l3]][[l4]])){
                                tr[[l1]][[l2]][[l3]][[l4]] = list()
                            }
                            tr[[l1]][[l2]][[l3]][[l4]][[l5]] <- ""
						}
					}
				}
			}	
		}
		
		tr
  	})
 
    datasetInput <- reactive({
        kaka.qry("fish","")
    }) 


	termInput <- reactive({
        kaka.qry("tree","")
    })


	demoInput <- reactive({
        
        dat <- read.csv('http://web/report/lengthfrequencyob/?fmt=csv/', header=TRUE)
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
        cb_options <- names(kaka.qry("tree", ""))

        selected <- x
    })
  
    # The output$view depends on both the databaseInput reactive
    # expression and input$obs, so will be re-executed whenever
    # input$dataset or input$obs is changed. 
    output$seafoodview <- renderDataTable({
		selected <- unlist(get_selected(input$tree))
		selected <- get_seafood_headers(selected)
        #stop(selected)
        ds <- datasetInput()
		ds.names = names(ds)
        if(length(selected)>0){
		    sel <- intersect(selected,ds.names)
		    sel <- c("name",  sel)
            ds[,sel]
        }
        else{
		    ds
        }
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




