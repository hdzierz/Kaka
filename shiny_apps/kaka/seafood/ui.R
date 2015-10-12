library(shiny)
library(shinyTree)

# Define UI for dataset viewer application
shinyUI(fluidPage(
    tags$head(tags$script(src="selectall.js")),
    title = "Fish Reports",
    titlePanel("Fish Reports"),

    sidebarLayout(
        # Sidebar with controls to provide a caption, select a dataset,
        # and specify the number of observations to view. Note that
        # changes made to the caption in the textInput control are
        # updated in the output area immediately as you type
        sidebarPanel(
			width=2,
            conditionalPanel(
            	'input.reports === "Seafood Base Reports"',
                downloadButton('downloadData', 'Download'),
				#br(),br(),
				#shinyTree("datasource", checkbox = TRUE, search=TRUE),
				br(), br(),
				shinyTree("tree", checkbox = TRUE, search=TRUE)
            ),
			conditionalPanel(
                'input.reports === "Seafood Demo Reports"',
                selectInput("group", "Group by:", choices=c("None", "Species","Gear", "Area", "Treatment", "Vessel"), selected="Area", width='100px')
			)
        ),
        # Show the caption, a summary of the dataset and an HTML
        # table with the requested number of observations
        mainPanel(
            tabsetPanel(
                id = 'reports',
                tabPanel('Seafood Base Reports', dataTableOutput('seafoodview')),
				tabPanel('Seafood Terms', dataTableOutput('seafoodterms')),
                tabPanel('Seafood Demo Reports', plotOutput('seafooddemo'))
            )
        )
    )
))
