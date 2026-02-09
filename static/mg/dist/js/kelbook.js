$(document).ready(function(){  

// user login 
	$("#login_form").on("submit",function(event){
		event.preventDefault();
		 $("#login_msg").html('<h4 class="text-center"><b class="text-info">Please wait...</b></h4>');
		
		$.ajax({
			url	:	"login.php",
			method:	"POST",
			data	:$("#login_form").serialize(),
			success	:function(data){
				$("#login_msg").html(data);
					
			}
		})
	})

// end of user login 

// user new staff 
	$("#add_staff_form").on("submit",function(event){
		event.preventDefault();
		 $("#add_msg").html('<center><img src="dist/img/loading.gif" width="70px"  /></center>');
		
		$.ajax({
			url	:	"mg_actions.php",
			method:	"POST",
			data	:$("#add_staff_form").serialize(),
			success	:function(data){
				$("#add_msg").html(data);
				setTimeout(location.reload.bind(location), 3000);
					
			}
		})
	})

// end of add new customers


// leads convertion 
	$("#lead_convertion").on("submit",function(event){
		event.preventDefault();
		 $("#lead_msg").html('<center><img src="dist/img/loading.gif" width="70px"  /></center>');
		
		$.ajax({
			url	:	"mg_actions.php",
			method:	"POST",
			data	:$("#lead_convertion").serialize(),
			success	:function(data){
				$("#lead_msg").html(data);
				setTimeout(location.reload.bind(location), 2000);
					
			}
		})
	})

// end of leads convertion

// All packages
packages();
function packages(){
	 $("#packages").html('<p <center><img src="app-assets/images/loading.gif"   /><center></p>');
		
		$.ajax({
			url	:	"mg_actions.php",
			method:	"POST",
			data	:	{all_packages:1},
			success	:function(data){
				$("#packages").html(data);
				
					
			}
		})

}
// end all packages

// add packages 
	$("#add_package_form").on("submit",function(event){
		event.preventDefault();
		 $("#pack_msg").html('<center><img src="dist/img/loading.gif" width="70px"  /></center>');
		
		$.ajax({
			url	:	"mg_actions.php",
			method:	"POST",
			data	:$("#add_package_form").serialize(),
			success	:function(data){
				$("#pack_msg").html(data);
				packages();
				// setTimeout(location.reload.bind(location), 2000);
					
			}
		})
	})

// end add package

// update packages 
	$("#update_package_form").on("submit",function(event){
		event.preventDefault();
		 $("#pack_msg").html('<center><img src="dist/img/loading.gif" width="70px"  /></center>');
		
		$.ajax({
			url	:	"mg_actions.php",
			method:	"POST",
			data	:$("#update_package_form").serialize(),
			success	:function(data){
				$("#pack_msg").html(data);
				packages();
				// setTimeout(location.reload.bind(location), 2000);
					
			}
		})
	})

// end update package

// delete invoice
$("body").delegate(".delete_package","click",function(){
		var pack_id = $(this).attr("pack");

	  if(confirm('Are you sure you want to delete package ?'))
        {
        	
            $.ajax({
               url: 'mg_actions.php',
                 method	:	"POST",
				 data	:	{DeletePackage:1,pack_id:pack_id},
               error: function() {
                  alert('Something is wrong ');
               },
            
			success	:	function(data){
				$("del_msg").html(data);
				packages();
				// setTimeout(location.reload.bind(location), 3000);
			}

			});
        }
		
	})
// end delete package






});