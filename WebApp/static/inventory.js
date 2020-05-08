$(document).ready(function(){
		function constructPaginationOld(itemsPerPage, rows){
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
		
		function constructPagination(itemsPerPage, rows){
			var rowsLength = rows.length;
			var totalPages = Math.ceil(rowsLength / itemsPerPage);
			
			
			if(totalPages > $(".pagination li.current-page").length){
				var newLength = totalPages;
				var currentLength = $(".pagination li.current-page").length;
				if(currentLength < newLength){
					
					for(i=currentLength; i < newLength; i++){
						if(i != 1){
							$(".pagination").append("<li class='page-item current-page'><a class='page-link' href='#'>"+ i +"</a></li>");
						}
					}
				}
			}
			
			$(".pagination li.current-page").each(function(){
				if($(this).text() != "1" && parseInt($(this).text()) > totalPages){
					$(this).hide();
				}
			});
			
		}
		
		function renderPage(grandTotal, itemsPerPage, rows){
			for(var i = 0; i < rows.length; i++){
				if(i < grandTotal - itemsPerPage || i > grandTotal -1){
					rows[i].style.display = "none";
				}//endIf
			}//endFor
		}//endFunction
	
		function getFilters(group){
			var filters = []
			switch (group){
				case 'Manufacturer':
					$('#manList li input:checkbox:not(:checked)').each(function(){
						filters.push($(this).parent().text());
					});
					break;
				case 'Model':
					$('#modList li input:checkbox:not(:checked)').each(function(){
						filters.push($(this).parent().text());
					});
					break;
				case 'Category':
					$('#catList li input:checkbox:not(:checked)').each(function(){
						filters.push($(this).parent().text());
					});
					break;
				case 'Reference Item':
					$('#refList li input:checkbox:not(:checked)').each(function(){
						filters.push($(this).parent().text());
					});
					break;
			}
			return filters
		}
		
		function searchFilter(term){
			
				// Search for term
			$(".divItems:visible").each(function(){
				// Manufacturer
				if($(this).find('.itemManufacturer').text().toLowerCase().match(term.toLowerCase()) == null){
					// Model
					if($(this).find('.itemModel').text().toLowerCase().match(term.toLowerCase()) == null){
						// Category
						if($(this).find('.itemCategory').text().toLowerCase().match(term.toLowerCase()) == null){
							// Reference Item
							if($(this).find('.refItem').text().toLowerCase().match(term.toLowerCase()) == null){
								// Item Name
								if($(this).find('.itemName').text().toLowerCase().match(term.toLowerCase()) == null){
									// Details
									if($(this).find(".itemDetails").text().toLowerCase().match(term.toLowerCase()) == null){
										// Serial Number
										if($(this).find(".itemSN").text().toLowerCase().match(term.toLowerCase()) == null){
											// Part Number
											if($(this).find(".itemPN").text().toLowerCase().match(term.toLowerCase()) == null){
												// Location Id
												if($(this).find(".itemLocationId").text().toLowerCase().match(term.toLowerCase()) == null){
													// SAP Id
													if($(this).find(".itemSapId").text().toLowerCase().match(term.toLowerCase()) == null){
														// vendor
														if($(this).find(".itemVendor").text().toLowerCase().match(term.toLowerCase()) == null){
															// Last Cost
															if($(this).find(".itemLastCost").text().toLowerCase().match(term.toLowerCase()) == null){

																$(this).hide();
															}
														}
													}
												}
											}
										}
									}
								}
							}
						}
					}
				}
			});
			filteredItems =  $(".divItems:visible");
			
			
			
			return filteredItems;
			
		}
		
		function applyFilters(){
			
			
				// Get Filters
			var manFilters = getFilters('Manufacturer');
			var modFilters = getFilters('Model');
			var catFilters = getFilters('Category');
			var refFilters = getFilters('Reference Item');
			
				// Apply Filters
			$(".divItems").each(function(){
				// Manufacturer
				for(i=0;i < manFilters.length; i++){
					if(manFilters[i] == $(this).find(".itemManufacturer").text()){
						
						$(this).hide();
					}
				}

				// Model
				console.log(modFilters);
				for(i=0; i < modFilters.length; i++){
					if(modFilters[i] == $(this).find('.itemModel').text()){
						
						$(this).hide();
					}
				}
				
				// Category
				for(i=0; i < catFilters.length; i++){
					if(catFilters[i] == $(this).find('.itemCategory').text()){
						
						$(this).hide();
						
					}
				}
				
				// Reference Item
				for(i=0; i < refFilters.length; i++){
					if(refFilters[i] == $(this).find('.itemRef').text()){
						
						$(this).hide();
						
					}
				}
				
			});
			var filteredItems =  $(".divItems:visible");
			
			
			return filteredItems;
		}
		
			// init pagination
		var items = []
		items = $('.divItems');
		var filteredItems = items;
		var itemsPerPage = 2;
		var currentPage = 1;
		
		/*
		//$(".pagination").append("<li id='previous' class='page-item'><a class='page-link' href='#'>Previous</a></li>");
		$(".pagination").append("<li class='page-item current-page active'><a class='page-link' href='#'>1</a></li>");
		//$(".pagination").append("<li id='next' class='page-item'><a class='page-link' href='#'>Next</a></li>");
		constructPagination(itemsPerPage, items);
		
		// Show items for page.
		var grandTotal = itemsPerPage * 1;
		renderPage(grandTotal, itemsPerPage, items);
		*/
		
			// Functionality of pagination
		/*$("#previous").click(function(){
			console.log('TEST PREVIOUS');
			var pages = $(".pagination").find("li.current-page");
			var currentPage = $(".pagination li.active");
			var currentPageIndex = pages.index(currentPage);
			
				// remove old active class and apply it to new current page.
			var previousIndex = currentPageIndex -1;
			currentPage.removeClass("active");
			pages.eq(previousIndex).addClass("active");
			
				// Show item for page
			grandTotal = itemsPerPage * (previous);

			renderPage(grandTotal, itemsPerPage, filteredItems);
			
		});
		
		$("#next").click(function(){
			console.log("TEST NEXT");
			
			var pages = $(".pagination").find("li.current-page");
			var currentPage = $(".pagination li.active");
			var currentPageIndex = pages.index(currentPage);
			
				// remove old active class and apply it to new current page.
			if(currentPageIndex < pages.length -1){
				var nextPageIndex = currentPageIndex + 1;
			}else{
				var nextPageIndex = 0;
			}
			currentPage.removeClass("active");
			pages.eq(nextPageIndex).addClass("active");
			
				// Show items for page
			
		});*/
		
		/*
		$(".pagination").find("li.current-page").click(function(){
			console.log("Test Page");
			
			var pages = $(".pagination").find("li.current-page");
			var currentPage = $(".pagination li.active");
			var currentPageIndex = pages.index(currentPage);
			var selectedPageIndex = pages.index($(this));
			
				// Show all items
			filteredItems.each(function(){
				$(this).show();
			});
			
			
				// remove old active and apply new active class.
			pages = $(".pagination").find("li.current-page");
			selectedPage = pages.eq(selectedPageIndex);
			
			pages.eq(currentPageIndex).removeClass("active");
			selectedPage.addClass("active");

			
				// Show items for page.
			var visibles = filteredItems;
			grandTotal = itemsPerPage * (selectedPageIndex + 1);

			renderPage(grandTotal, itemsPerPage, visibles);
			
		});
		*/
		
			// Set part numbers, serial numbers, location id, details, SAP id, vendor, and lastCost.
		$(".itemSN").parent().hide();
		$(".itemSN").each(function(){

			$(this).hide();
		});
		$(".itemPN").each(function(){

			$(this).hide();
		});
		$(".itemLocationId").each(function(){

			$(this).parent().hide();
		});
		$(".itemDetails").each(function(){

			$(this).hide();
		});
		$(".itemSapId").each(function(){

			$(this).hide();
		});
		$(".itemVendor").each(function(){

			$(this).hide();
		});

		
		// Check for non-checked checkboxes for:
		$('#btnFilter').click(function(){
			
				// Show all items
			$(".divItems").each(function(){
				$(this).show();
			});
			
			// Apply filters
			filteredItems = applyFilters();
			
			// Apply search filter
			term = $("#txtId").val().toString();
			if(term != null || term != ""){
				filteredItems = searchFilter(term);
			}
			/*
			constructPagination(itemsPerPage, filteredItems);
			
			grandTotal = itemsPerPage * 1;
			renderPage(grandTotal, itemsPerPage, filteredItems);
			console.log(grandTotal);
			*/
		});
		
		// hide data based on filter.
		$(".btnSearch").click(function(){
			
				// Show all items
			$(".divItems").each(function(){
				$(this).show();
			});
			
			// Apply search filter
			var term = $('#txtId').val().toString();
			if(term != null || term != ""){
				filteredItems = searchFilter(term);
			}
			
			// Apply filters
			filteredItems = applyFilters();
			
			/*
			// pagination
			constructPagination(itemsPerPage, filteredItems);
			
			var grandTotal = itemsPerPage * 1;
			renderPage(grandTotal, itemsPerPage, filteredItems);
			*/
		});
	
});