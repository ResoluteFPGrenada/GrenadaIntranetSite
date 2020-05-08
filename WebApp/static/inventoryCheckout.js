$(document).ready(function(){
			
		// Add to Quantity Selected
	$(".itemQuantity").find(".quantityAdd").click(function(){
		var $parent = $(this).parent().parent();
		var value = Number($parent.find(".quantity").text());
		
		var $subparent = $parent.parent();
		var inStock = Number($subparent.find(".stockQuantity h3").text());
		
		if(inStock > value){
			value = value + 1
			$parent.find(".quantity").text(parseInt(value));
		}
	});
	
		// Subtract from Quantity Selected
	$(".itemQuantity").find(".quantitySub").click(function(){
		var $parent = $(this).parent().parent();
		var value = Number($parent.find(".quantity").text());
		
		if($parent.find(".quantity").text() != "0"){
			value = value - 1;
			$parent.find(".quantity").text(parseInt(value));
		}
	});
	
		// Complete Checkout On Click
	$("#btnCompleteCheckout").click(function(){
		var objs = []
		$(".quantity").each(function(i){
			
			var itemId = $(this).attr("id").replace("quantity",""); 
			var selectedQuantity = $(this).text();
			
			var obj = {
				itemId : itemId,
				quantity : selectedQuantity
			}
			objs.push(obj);
		});
		var json = JSON.stringify(objs);
		
			// Send data to completeCheckout url with json data 
		//window.location('http://10.42.50.22:5000/pc/');
		var url = window.location.href;
		var newUrl = url.replace('checkout','completeCheckout/' + json);
		/*$.ajax({
			type : "POST",
			url : newUrl,
			data : json,
			cache: false,
			success: function(data){
				$.ajax({
					type: "POST",
					url: newUrl,
					data: json,
					cache:false
				});
			}
		});*/

		window.location.href = newUrl;
	});
});