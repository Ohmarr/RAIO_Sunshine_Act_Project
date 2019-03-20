var currentDoctor; // global variables; 

var allDoctors = {};

function init() { 			// Visit '/names' ⟶ default route (app.py)
	var selector = d3.select("#selDataset"); // dropdown selector
	var default_url = '/names';

	d3.json(default_url).then( // Parameter=JSON list of names
		doctorNames => {
			doctorNames.forEach(
				name => {
					selector
						.append("option") // append options for dropdown selection
						.text(name.Name)     // add text
						.property("value", name.Name);
				});
			var nameSelected = doctorNames[0]; // 1st Sample
			newSelection(nameSelected)
			console.log(nameSelected)
		});	   // Return ⟶ Function Calls buildCharts(firstSample) & buildTable(firstSample);

};					// Operations ⟶ Adds sample options to # & Returns 1 ⟶ Calls buildCharts(1) & buildTable(1);

function newSelection(drName) {	//  Dropdown Change ⟶ New Sample Selected
	console.log("doctor = ", drName)
	console.log('url = ', `/names/${drName}`)
	if (typeof (drName) != "string"){
		drName = drName.Name
	}
	d3.json(`/names/${drName}`)
		.then(
			drInfoData => {
				currentDoctor = drInfoData;
				buildTable(drInfoData)
				buildCharts(drInfoData)
				buildMap(drInfoData)
				console.log(drInfoData)
			})
}; 					// Return ⟶ function calls ⟶ buildCharts(newName) & buildTable(newName);

function buildTable(drInfo) { 	// access key/value pairs from @ nameData route & construct panel  
	
	var drPanel = d3.selectAll('.panel-body')
	drPanel.selectAll('p').html('')  // clear drPanel to prepare for new data; 
	drPanel.append('p')
		.html(`
			ID: ${drInfo[0].Physician_ID},\n
			Name: ${drInfo[0].Name},\n
			State: ${drInfo[0].State},\n
			Zip Code: ${drInfo[0].ZipCode},\n
			GPO Name: ${drInfo[0].GPO_Name},\n
			Payment_Name: ${drInfo[0].Payment_Name},\n
			Amount: ${drInfo[0].Amount},\n
			Transaction Date: ${drInfo[0].PaymentDate},\n
			Number of Payments: ${drInfo[0].NumberofPayment},\n
			Form of payment: ${drInfo[0].Formofpayment},\n
			Nature: ${drInfo[0].Nature},\n
			Primary Key: ${drInfo[0].pk_column}.\n`
			)
	// Object.entries(drInfo).forEach(([key, value])=>console.log(key + ':' + value));
};					// Return ⟶ nameData Panel

function buildCharts(drInfo) { 		// build Pie Chart
	var trace_pie = {
		values: drInfo.Amount,	// performed in pd df//.slice(0,10),
		labels: drInfo.Nature,         // performed in pd df//.slice(0,10),
		type: 'pie'
	};
	var data_pie = [trace_pie]; //data must be an array; so converted here; 
	var layout_pie = {
		title: "'Pie' Chart - Dr Info",
		height: 400,
		width: 500
	};
	Plotly.newPlot('pie', data_pie, layout_pie); // pie chart

	var trace1 = {
		x: drInfo.Amount, // 
		y: drInfo.Nature,
		text: drInfo.State,
		mode: 'markers',
		marker: {
		  size: drInfo.Amount,
		 // color: blue
		}
	      };
	      
	var data = [trace1];
	      
	var layout = {
		title: 'Marker Size',
		showlegend: false,
		height: 500,
		width: 1000
	      };
	      
	Plotly.newPlot('bubble', data, layout);
};					// // Return ⟶ append each chart to html

function buildMap(drInfo){

}

init();					// Return ⟶ Function Call init()
