
$(document).ready(function(){
	
	var table = document.getElementById('tblLogs');
	var rows = table.getElementsByTagName('tr');
	var itemsPerPage = 100;
	var currentPage = 1;
	
	// init pagination
	constructPagination(itemsPerPage, rows);

	// init sort to pages.
	var grandTotal = itemsPerPage * currentPage;
		
	renderPage(grandTotal, itemsPerPage, rows);
	
	
		// filter searches
	$('#searchId, #searchUser, #searchDateTo, #searchTimeTo, #searchSupervisor, #searchEventLocation, #searchEventType, #searchComment').on('keyup', function(){

		id = document.getElementById('searchId').value;
		user = document.getElementById('searchUser').value.toLowerCase();
		fDate = document.getElementById('searchDateFrom').value;
		tDate = document.getElementById('searchDateTo').value;
		fTime = document.getElementById('searchTimeFrom').value;
		tTime = document.getElementById('searchTimeTo').value;
		supervisor = document.getElementById('searchSupervisor').value.toLowerCase();
		eLocation = document.getElementById('searchEventLocation').value.toLowerCase();
		eType = document.getElementById('searchEventType').value.toLowerCase();
		comment = document.getElementById('searchComment').value.toLowerCase();
		
		searchId(id, user, fDate, tDate, fTime, tTime, supervisor, eLocation, eType, comment, rows);

			// get current visible logs
		var $visibles = $("#tblLogs tr:visible");
		
			// structure pagination
		constructPagination(itemsPerPage,$visibles);
		
			// inside loop pagination selection
		$(".pagination li.current-page").on('click', function(){
			id = document.getElementById('searchId').value;
			user = document.getElementById('searchUser').value.toLowerCase();
			fDate = document.getElementById('searchDateFrom').value;
			tDate = document.getElementById('searchDateTo').value;
			fTime = document.getElementById('searchTimeFrom').value;
			tTime = document.getElementById('searchTimeTo').value;
			supervisor = document.getElementById('searchSupervisor').value.toLowerCase();
			eLocation = document.getElementById('searchEventLocation').value.toLowerCase();
			eType = document.getElementById('searchEventType').value.toLowerCase();
			comment = document.getElementById('searchComment').value.toLowerCase();
			
			searchId(id, user, fDate, tDate, fTime, tTime, supervisor, eLocation, eType, comment, rows);

			
			if($(this).hasClass('active')){
				return false;
			}else{
				var currentPage = $(this).index();
				$(".pagination li").removeClass('active');
				$(this).addClass("active");
				
				var grandTotal = itemsPerPage * currentPage;
			
				renderPage(grandTotal, itemsPerPage, $visibles);
			}//endIf/Else

		});//endClickEvent
		
			//inside loop pagination selection Next
		$("#next").on("click", function(){
				//get filtered rows again
			id = document.getElementById('searchId').value;
			user = document.getElementById('searchUser').value.toLowerCase();
			fDate = document.getElementById('searchDateFrom').value;
			tDate = document.getElementById('searchDateTo').value;
			fTime = document.getElementById('searchTimeFrom').value;
			tTime = document.getElementById('searchTimeTo').value;
			supervisor = document.getElementById('searchSupervisor').value.toLowerCase();
			eLocation = document.getElementById('searchEventLocation').value.toLowerCase();
			eType = document.getElementById('searchEventType').value.toLowerCase();
			comment = document.getElementById('searchComment').value.toLowerCase();
			
			searchId(id, user, fDate, tDate, fTime, tTime, supervisor, eLocation, eType, comment, rows);

			
				// select Next index of pages
			numberOfPages = $(".pagination li.current-page").length;
			currentPage = $(".pagination").find("li.active").index();
			if(currentPage == numberOfPages){
				currentPage = 1;
			}else{
				currentPage = currentPage +1;
			}
			
				// remove old active and apply new active class.
			newPage = $(".pagination li").eq(currentPage);
			$(".pagination li").removeClass('active');
			newPage.addClass("active");
			
				// filter rows
			var grandTotal = itemsPerPage * currentPage;
			renderPage(grandTotal, itemsPerPage, $visibles);
		});
		
			//inside loop pagination selection Previous
		$("#previous").on('click', function(){
				//get filtered rows again
			id = document.getElementById('searchId').value;
			user = document.getElementById('searchUser').value.toLowerCase();
			fDate = document.getElementById('searchDateFrom').value;
			tDate = document.getElementById('searchDateTo').value;
			fTime = document.getElementById('searchTimeFrom').value;
			tTime = document.getElementById('searchTimeTo').value;
			supervisor = document.getElementById('searchSupervisor').value.toLowerCase();
			eLocation = document.getElementById('searchEventLocation').value.toLowerCase();
			eType = document.getElementById('searchEventType').value.toLowerCase();
			comment = document.getElementById('searchComment').value.toLowerCase();
			
			searchId(id, user, fDate, tDate, fTime, tTime, supervisor, eLocation, eType, comment, rows);

			
				// select previous index of pages
			numberOfPages = $(".pagination li.current-page").length;
			currentPage = $(".pagination").find("li.active").index();
			if(currentPage <= 1){
				currentPage = numberOfPages;
			}else{
				currentPage = currentPage -1;
			}
			
				// remove old active and apply new active class.
			newPage = $(".pagination li").eq(currentPage);
			$(".pagination li").removeClass('active');
			newPage.addClass("active");
			
				// filter rows
			var grandTotal = itemsPerPage * currentPage;
			renderPage(grandTotal, itemsPerPage, $visibles);

		});//endCLickEvent
	});//endClickEvent
	
		// outside loop pagination selection Next
	$("#next").on("click",function(){
		currentPage = $(".pagination").find("li.active").index();
		
			// select Next index of pages
		numberOfPages = $(".pagination li.current-page").length;
		currentPage = $(".pagination").find("li.active").index();
		if(currentPage == numberOfPages){
			currentPage = 1;
		}else{
			currentPage = currentPage +1;
		}
		
			// remove old active and apply new active class.
		newPage = $(".pagination li").eq(currentPage);
		$(".pagination li").removeClass('active');
		newPage.addClass("active");
		
			// filter rows
		var rows = $("#tblLogs tr");
		for(var i = 0; i < rows.length; i++){
			rows[i].style.display = "";
		}
			
		var grandTotal = itemsPerPage * currentPage;
		renderPage(grandTotal, itemsPerPage, rows);
	});
	
		// outside loop pagination selection Previous
	$("#previous").on('click', function(){
		currentPage = $(".pagination").find("li.active").index();
		
			// select previous index of pages
		numberOfPages = $(".pagination li.current-page").length;
		currentPage = $(".pagination").find("li.active").index();
		if(currentPage <= 1){
			console.log("test");
			currentPage = numberOfPages;
		}else{
			currentPage = currentPage -1;
		}
		
			// remove old active and apply new active class.
		newPage = $(".pagination li").eq(currentPage);
		$(".pagination li").removeClass('active');
		newPage.addClass("active");
		
			// filter rows
		var rows = $("#tblLogs tr");
		for(var i = 0; i < rows.length; i++){
			rows[i].style.display = "";
		}
			
		var grandTotal = itemsPerPage * currentPage;
		renderPage(grandTotal, itemsPerPage, rows);
	});

		// outside loop pagination selection
	$(".pagination li.current-page").on('click', function(){
		if($(this).hasClass('active')){
			return false;
		}else{
			var currentPage = $(this).index();
			$(".pagination li").removeClass('active');
			$(this).addClass("active");
		
			var rows = $("#tblLogs tr");
			for(var i = 0; i < rows.length; i++){
				rows[i].style.display = "";
			}
			var grandTotal = itemsPerPage * currentPage;
			
			renderPage(grandTotal, itemsPerPage, rows);
		}//endIf/Else
		
	});//endClickEvent
	
});//endJquery

function renderPage(grandTotal, itemsPerPage, rows){
	for(var i = 0; i < rows.length; i++){
		if(i < grandTotal - itemsPerPage || i > grandTotal -1){
			rows[i].style.display = "none";
		}//endIf
	}//endFor
}//endFunction

function constructPagination(itemsPerPage, rows){
	var rowsLength = rows.length;
	var totalPages = Math.ceil(rowsLength / itemsPerPage);
	
	$(".pagination").empty();
	
	$(".pagination").append("<li id='previous' class='page-item'><a class='page-link' href='#'>Previous</a></li>");
	$(".pagination").append("<li class='page-item current-page active'><a class='page-link' href='#'>1</a></li>");
	
	if(totalPages >= 2){
		for(i=2; i <= totalPages; i++){
			$(".pagination").append("<li class='page-item current-page'><a class='page-link' href='#'>"+ i +"</a></li>");
		}//endFor
	}//endIf
	
	$(".pagination").append("<li id='next' class='page-item'><a class='page-link' href='#'>Next</a></li>");
	
}//endFunction

function searchId(id, user, fDate, tDate, fTime, tTime, supervisor, eLocation, eType, comment, tr){
	var filters = [id, user, tDate, tTime, supervisor, eLocation, eType, comment, fDate, fTime];
	var trs = new Array(tr);
	for(i=0; i < tr.length; i++){
		tr[i].style.display = "";
	}//end-for
	
		for (var i=0; i < filters.length; i++){

			if(filters[i] == ""){
				console.log("its blank");
			}else if(i == 2){
				
				if(filters[i].match(/^(\d{4})\-(\d{2})\-(\d{2})$/) != null && filters[8].match(/^(\d{4})\-(\d{2})\-(\d{2})$/) != null){
					var toDate = new Date(filters[i]);
					var fromDate = new Date(filters[8]);

					for(j=0; j < trs[0].length; j++){
						if(trs[0][j].style.display == ""){
							var td = trs[0][j].getElementsByTagName('td')[i];
							
							if(td){
								var txtValue = td.textContent || td.innerText;
								txtValue = new Date(txtValue);

								if(txtValue.getTime() >= fromDate.getTime() && txtValue.getTime() <= toDate.getTime()){
									
								}else{
									trs[0][j].style.display = "none";
								}//end-if
							}//end-if
						}//end-if
					}//end_for
				}//end-if
				
			}else if(i == 3){
				
				if(filters[i].match(/^(\d{2}):(\d{2}):(\d{2})$/) != null && filters[9].match(/^(\d{2}):(\d{2}):(\d{2})$/) != null){
					var tempToTime = filters[i].split(":");
					
					//tempToTime = [2018,10,10,parseInt(tempToTime[0], 10), parseInt(tempToTime[1], 10)];
					var tempFromTime = filters[9].split(":");
					
					var toTime = new Date(2018,1,2,parseInt(tempToTime[0]), parseInt(tempToTime[1]));
					var fromTime = new Date(2018,1,2,parseInt(tempFromTime[0]), parseInt(tempFromTime[1]));
					
					for(j=0; j < trs[0].length; j++){
						if(trs[0][j].style.display == ""){
							var td = trs[0][j].getElementsByTagName('td')[i];
							
							if(td){
								var txtValue = td.textContent || td.innerText;
								var tempTextValue = txtValue.split(":");
								txtValue = new Date(2018,1,2,tempTextValue[0],tempTextValue[1]);
								
								if(txtValue.getTime() >= fromTime.getTime() && txtValue.getTime() <= toTime.getTime()){
									
								}else{
									trs[0][j].style.display = "none";
								}//end-if/else
							}//end-if
						}//end-if
					}//end-for
					console.log("Its a Time");
				}//end-if
				
			}else if(i != 9 && i != 8){
				
				for(var j=0; j< trs[0].length; j++){
					if(trs[0][j].style.display == ""){
						var td = trs[0][j].getElementsByTagName('td')[i];

						if(td){
							var txtValue = td.textContent || td.innerText;
							if(txtValue.toLowerCase().indexOf(filters[i]) > -1){}else{
								trs[0][j].style.display = "none";
								
							}//end-if/else
						}//end-if
					}//end-if
				}//end-for
				
			}//end-if/else
		}//end-for

}// END_FUNCTION