		$(document).ready(function(){
				// change header and initiate task filtering
			$('#nav2 a').on('click',function(){
				var element = $(this).text();
				var exists = document.getElementById('maintAdmin');
				$('#contentHeader').text(element);
				
				fetch('/tasks/'+ element +'/json').then(function(response){
					response.json().then(function(data){
						
							// set contentheader to element
						$('#contentHeader').text(element);
						//console.table(data);
						
							// set tabs based on data
						$('#modArea').html('');
						$('#nav').html('');
						$('#tblEquip').html('');
						$('#tblItem').html('');
						$('#tblTask').html('');
						for (i = 0; i < data.length; i++){
								$('#nav').append('<li class="nav-item"><a id="aArea'+ data[i].id +'" class="nav-link active" data-toggle="tab" href="#area'+ data[i].id +'">'+ data[i].name +'</a></li>');
								
								$('.divModal').append('<div class="modal fade" id="deleteModalAreas'+data[i].id+'" tabindex="-1" role="dialog" aria-labelledby="deleteModalAreaslabel" aria-hidden="true">'+
													'<div class="modal-dialog" role="document">'+
														'<div class="modal-content">'+
															'<div class="header">'+
																'<h5 class="modal-title" id="deleteModalAreasLabel'+data[i].id+'">Delete Link</h5>'+
																'<button type="button" class="close" data-dismiss="modal" aria-label="Close">'+
																	'<span aria-hidden="true">&times;</span>'+
																'</button>'+
															'</div>'+
															'<div class="modal-footer">'+
																'<button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>'+
																	'<form action="/tasks/delete/area/'+data[i].id+'">'+
																		'<input class="btn btn-danger" type="submit" value="Delete">'+
																	'</form>'+
																'</button>'+
															'</div>'+
														'</div>'+
													'</div>'+
												'</div>');
						}//end for
						if(exists){
							$('#nav').append('<li class="nav-item bg-info"><a class="nav-link text-white" href="/tasks/new/area">+</a></li>');
						}
						
							// set equipment based on clicked area
						$('ul.nav li').click(function(e){
							$('#modArea').html('');
							$('#tblEquip').html('');
							$('#tblItem').html('');
							$('#tblTask').html('');
							var eleId = e.target.id;
							eleId = eleId.replace("aArea","");
							eleId = parseInt(eleId);
							current_area = data.find(function(area){
								if(area.id === eleId){return area}
							});
							if(exists){
								$('#modArea').append('<a class="btn btn-sm btn-secondary" role="button" href="/tasks/update/area/'+ eleId +'">Update Area</a>');
								$('#modArea').append('<button type="button" class="btn btn-danger btn-sm m-1" data-toggle="modal" data-target="#deleteModalAreas'+ eleId +'">Delete Area</button>');
							}
							for(i=0; i < current_area.equipment.length; i++){
								if(exists){

									$('#tblEquip').append('<tr><td id="equip'+ current_area.equipment[i].id +'">' + current_area.equipment[i].title +'</td>'+
										'<td><a class="btn btn-secondary btn-sm mt-1 mb-1" href="/tasks/update/equipment/'+ current_area.equipment[i].id +'">Update</a></td>'+
										'<td><button type="button" class="btn btn-danger btn-sm m-1" data-toggle="modal" data-target="#deleteModalEquip'+ current_area.equipment[i].id +'">Delete</button></td></tr>' );
										
									$('.divModal').append('<div class="modal fade" id="deleteModalEquipment'+current_area.equipment[i].id+'" tabindex="-1" role="dialog" aria-labelledby="deleteModalEquipmentlabel" aria-hidden="true">'+
													'<div class="modal-dialog" role="document">'+
														'<div class="modal-content">'+
															'<div class="header">'+
																'<h5 class="modal-title" id="deleteModalEquipmentLabel'+current_area.equipment[i].id+'">Delete Link</h5>'+
																'<button type="button" class="close" data-dismiss="modal" aria-label="Close">'+
																	'<span aria-hidden="true">&times;</span>'+
																'</button>'+
															'</div>'+
															'<div class="modal-footer">'+
																'<button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>'+
																	'<form action="/tasks/delete/equipment/'+current_area.equipment[i].id+'">'+
																		'<input class="btn btn-danger" type="submit" value="Delete">'+
																	'</form>'+
																'</button>'+
															'</div>'+
														'</div>'+
													'</div>'+
												'</div>');
								}else{
									$('#tblEquip').append('<tr><td id="equip'+ current_area.equipment[i].id +'">' + current_area.equipment[i].title + '</td></tr>');
								}//end if/else
							}//end for
							
								// set items based on clicked equipment
							$('tbody[id*=tblEquip] tr').click(function(e){
								$('#tblItem').html('');
								$('#tblTask').html('');
								var eleEId = e.target.id;
								eleEId = eleEId.replace("equip","");
								eleEId = parseInt(eleEId);
								//current_equip = current_area.equipment.find(equip => equip.id === eleEId);
								current_equip = current_area.equipment.find(function(equip){
									if(equip.id === eleEId){return equip}
								});
								for(i=0; i < current_equip.items.length; i++){
									if(exists){
										$('#tblItem').append('<tr class="select-tr"><td id="item'+ current_equip.items[i].id +'">'+ current_equip.items[i].name +'</td>'+
										' <td><a class="btn btn-secondary btn-sm mt-1 mb-1" href="/tasks/update/item/'+ current_equip.items[i].id +'">Update</a></td>'+
										' <td><button type="button" class="btn btn-danger btn-sm m-1" data-toggle="modal" data-target="#deleteModalItems'+ current_equip.items[i].id +'">Delete</button></td></tr>');
										
										$('.divModal').append('<div class="modal fade" id="deleteModalItems'+current_equip.items[i].id+'" tabindex="-1" role="dialog" aria-labelledby="deleteModalItemslabel" aria-hidden="true">'+
													'<div class="modal-dialog" role="document">'+
														'<div class="modal-content">'+
															'<div class="header">'+
																'<h5 class="modal-title" id="deleteModalItemsLabel'+current_equip.items[i].id+'">Delete Link</h5>'+
																'<button type="button" class="close" data-dismiss="modal" aria-label="Close">'+
																	'<span aria-hidden="true">&times;</span>'+
																'</button>'+
															'</div>'+
															'<div class="modal-footer">'+
																'<button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>'+
																	'<form action="/tasks/delete/item/'+current_equip.items[i].id+'">'+
																		'<input class="btn btn-danger" type="submit" value="Delete">'+
																	'</form>'+
																'</button>'+
															'</div>'+
														'</div>'+
													'</div>'+
												'</div>');
									}else{
										$('#tblItem').append('<tr><td id="item'+ current_equip.items[i].id +'">'+ current_equip.items[i].name +'</td></tr>');
									}//end if/else
								}//end for
								
									// set tasks based on clicked items
								$('tbody[id*=tblItem] tr').click(function(e){
									$('#tblTask').html('');
									var eleIId = e.target.id;
									eleIId = eleIId.replace("item","");
									eleIId = parseInt(eleIId);
									//current_item = current_equip.items.find(item => item.id === eleIId);
									current_item = current_equip.items.find(function(item){
										if(item.id === eleIId){return item}
									});
									
									for(i=0; i < current_item.tasks.length; i++){
										
										if(exists){
											$('#tblTask').append('<tr><td>'+ current_item.tasks[i].name +'</td>'+
												'<td>'+ current_item.tasks[i].date_due +'</td>'+
												'<td><a class="btn btn-success btn-sm mt-1 mb-1" href="/tasks/complete/'+ current_item.tasks[i].id +'">Mark As Complete</a></td>'+
												'<td><a class="btn btn-secondary btn-sm mt-1 mb-1" href="/tasks/update/task/'+ current_item.tasks[i].id +'">Update</a></td>'+
												'<td><button type="button" class="btn btn-danger btn-sm m-1" data-toggle="modal" data-target="#deleteModalTasks'+ current_item.tasks[i].id +'">Delete</button></td>'+									
												'</tr>');
												
											$('.divModal').append('<div class="modal fade" id="deleteModalTasks'+current_item.tasks[i].id+'" tabindex="-1" role="dialog" aria-labelledby="deleteModalTaskslabel" aria-hidden="true">'+
													'<div class="modal-dialog" role="document">'+
														'<div class="modal-content">'+
															'<div class="header">'+
																'<h5 class="modal-title" id="deleteModalTasksLabel'+current_item.tasks[i].id+'">Delete Link</h5>'+
																'<button type="button" class="close" data-dismiss="modal" aria-label="Close">'+
																	'<span aria-hidden="true">&times;</span>'+
																'</button>'+
															'</div>'+
															'<div class="modal-footer">'+
																'<button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>'+
																	'<form action="/tasks/delete/task/'+current_item.tasks[i].id+'">'+
																		'<input class="btn btn-danger" type="submit" value="Delete">'+
																	'</form>'+
																'</button>'+
															'</div>'+
														'</div>'+
													'</div>'+
												'</div>');
										}else{
											$('#tblTask').append('<tr><td class="">'+ current_item.tasks[i].name +'</td>'+
												'<td>'+ current_item.tasks[i].date_due +'</td>'+
												'<td><a class="btn btn-success btn-sm mt-1 mb-1" href="/tasks/complete/'+ current_item.tasks[i].id +'">Mark As Complete</td>'+
												'</tr>');
										}//end if/else
									}//end for
								});
							});
						});
							
					});
				});
				
			});
		});
			