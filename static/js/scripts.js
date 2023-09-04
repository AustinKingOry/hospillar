//this function does not relate to anything on this project. I was working on something prompt and needed a ready file
function isPangram(string) {
	const alph = 'abcdefghijklmnopqrstuvwxyz';
	const letters = new Set();
	const s = string.toLowerCase();
  
	for (let i = 0; i < s.length; i++) {
	  const char = s[i];
	  if (alph.includes(char)) {
		letters.add(char);
	  }
	}
  
	return letters.size === alph.length;
}

//this one too
function duplicateEncode(word){
	let new_arr=[]
	let w=(word).toLowerCase().split('');
	w.forEach(c=>{
	  if ((word.split(c).length - 1) >1){
		new_arr.push(')');
	  }
	  else{
		new_arr.push('(');
	  }
	});
	return((new_arr.toString()).replaceAll(',',''));
}

//end of unrelated functions
//handling the action buttons
var actionBtns=document.querySelectorAll('.actions-btn');
var actionWrappers=document.querySelectorAll('.actions-sect');
var dropdownBtns=document.querySelectorAll('.info-wrapper-toogle');        
var cardWrappers=document.querySelectorAll('.dropable-sect');

window.addEventListener('load',()=>{
    for(i=0;i<actionBtns.length;i++){
        actionBtns[i].setAttribute('onclick','hideActionsWrapper(\''+i+'\');');
    }
    for(i=0;i<dropdownBtns.length;i++){
        dropdownBtns[i].setAttribute('onclick','expandCardWrapper(\''+i+'\')')
    }
});
function hideActionsWrapper(index){
    if(actionWrappers[index].style.display=='none'){
        actionWrappers[index].style.display='flex';
    }
    else if(actionWrappers[index].style.display=='flex'){
        actionWrappers[index].style.display='none';
    }
    else{
        actionWrappers[index].style.display='flex';
    }
}
function expandCardWrapper(index){
    cardWrappers[index].classList.toggle('hidden');
    document.querySelectorAll('.gen-info-wrapper')[index].style.minHeight="fit-content";
    dropdownBtns[index].classList.toggle('bi-chevron-up');
    if(dropdownBtns[index].classList.contains('bi-chevron-up')){
        dropdownBtns[index].setAttribute('title','Maximize');
    }
    else if(dropdownBtns[index].classList.contains('bi-chevron-down')){                
        dropdownBtns[index].setAttribute('title','Minimize');
    }
}
//searching and sorting tables
var sortControls = document.querySelectorAll('.sort-control');
sortControls.forEach((sortcontrol,index) => {
    sortcontrol.addEventListener('click',()=>{
        if(sortcontrol.classList.contains('bi-sort-up')){
            sortcontrol.classList.replace('bi-sort-up','bi-sort-down-alt');
        }
        else if(sortcontrol.classList.contains('bi-sort-down-alt')){
            sortcontrol.classList.replace('bi-sort-down-alt','bi-sort-up');
        }
        else{
            sortcontrol.classList.add('bi-sort-up');
        }
    });
});
function searchTable() {
	var input, filter, table, tr, td, i, txtValue;
	input = document.getElementById("search-input");
	filter = input.value.toUpperCase();
	table = document.getElementById("main-table");
	// tr = table.getElementsByTagName("tr");
	tr = table.querySelectorAll(".row-items-wrapper");
	for (i = 0; i < tr.length; i++) {
		tr[i].style.display = "none";
		td = tr[i].getElementsByTagName("td");
		for (var j = 0; j < td.length; j++) {
			cell = tr[i].getElementsByTagName("td")[j];
			if (cell) {
				txtValue = td[j].textContent || td[j].innerText;
			if (txtValue.toUpperCase().indexOf(filter) > -1) {
				tr[i].style.display = "";
				if(input.value==''){
					paginate(10,1);
				}				
				break;
			} 
			else {
				tr[i].style.display = "none";
			}
			}
		}

	}
}
function sortTable(n) {
	var table, rows, switching, i, x, y, shouldSwitch, dir, switchcount = 0;
	table = document.getElementById("main-table");
	switching = true;
	// Set the sorting direction to ascending:
	dir = "asc";
	/* Make a loop that will continue until
	no switching has been done: */
	while (switching) {
		// Start by saying: no switching is done:
		switching = false;
		rows = table.rows;
		/* Loop through all table rows (except the
		first, which contains table headers): */
		for (i = 1; i < (rows.length - 1); i++) {
			// Start by saying there should be no switching:
			shouldSwitch = false;
			/* Get the two elements you want to compare,
			one from current row and one from the next: */
			x = rows[i].getElementsByTagName("TD")[n];
			y = rows[i + 1].getElementsByTagName("TD")[n];
			/* Check if the two rows should switch place,
			based on the direction, asc or desc: */
			if (dir == "asc") {
			if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
			// If so, mark as a switch and break the loop:
			shouldSwitch = true;
			break;
			}
			} else if (dir == "desc") {
			if (x.innerHTML.toLowerCase() < y.innerHTML.toLowerCase()) {
			// If so, mark as a switch and break the loop:
			shouldSwitch = true;
			break;
			}
			}
		}
		if (shouldSwitch) {
			/* If a switch has been marked, make the switch
			and mark that a switch has been done: */
			rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
			switching = true;
			// Each time a switch is done, increase this count by 1:
			switchcount ++;
		} else {
			/* If no switching has been done AND the direction is "asc",
			set the direction to "desc" and run the while loop again. */
			if (switchcount == 0 && dir == "asc") {
				dir = "desc";
				switching = true;
			}
		}
	}
}
if(document.querySelector('#main-table')){
	window.addEventListener('load',()=>{
		let rowsPerView = 10
		let table = document.querySelector('#main-table');
		let rows  = table.querySelectorAll('.row-items-wrapper');
		let rowsCount = rows.length;
		let element = document.querySelector(".pagination ul");
		let totalPages = Math.ceil(rowsCount/rowsPerView);
		let page = 1;
		if(totalPages>1){
			paginate(rowsPerView,1);
			element.innerHTML = createPagination(totalPages,page,rowsPerView);
		}		
	});
	if(document.getElementById('rpv-btn')){
		document.getElementById('rpv-btn').addEventListener('change',()=>{paginate(document.getElementById('rpv-btn').value,1)});
	}	
}

function paginate(rowsPerView,page_num){
	let table = document.querySelector('#main-table');
	let rows  = table.querySelectorAll('.row-items-wrapper');
	let rowsCount = rows.length;
	let maxValue = rowsPerView*page_num;
	let minValue = maxValue-rowsPerView;
	// let counter= [];
	let groups = Math.ceil(rowsCount/rowsPerView);
	if(rowsCount>=rowsPerView){
		rows.forEach((row,index)=>{
			// counter.push(index);
			if(index<maxValue&&index>=minValue){
				row.style.display=null;
			}
			else{
				row.style.display='none';
			}
		});
	}
	else{
		rows.forEach((row,index)=>{
			row.style.display=null;
		});
	}
	let rec_msg = `<span>Showing ${minValue} to ${maxValue} of ${rowsCount} entries.</span>`;
	document.getElementById('page-data-indicator').innerHTML = rec_msg;
	// console.log(counter,maxValue,minValue)
}
function createPagination(totalPages, page,rowsPerView){
	let element = document.querySelector(".pagination ul");
	let liTag = '';
	let active;
	let beforePage = page - 1;
	let afterPage = page + 1;
	if(page > 1){
		liTag += `<li class="btn prev" onclick="createPagination(${totalPages}, ${page - 1}, ${rowsPerView})"><span><i class="fas fa-angle-left"></i> Prev</span></li>`;
	}

	if(page > 2){
		// liTag += `<li class="first numb" onclick="createPagination(${totalPages}, 1)"><span>1</span></li>`;
		if(page > 3){
			liTag += `<li class="dots"><span>...</span></li>`;
		}
	}
	if(page == totalPages){
		beforePage = beforePage - 2;
	} 
	else if(page == totalPages - 1){
		beforePage = beforePage - 1;
	}
	if(page == 1) {
		afterPage = afterPage + 2;
	}
	else if(page == 2) {
		afterPage  = afterPage + 1;
	}

	for(var plength = beforePage; plength <= afterPage; plength++){
		if(plength > totalPages){
			continue;
		}
		if(plength == 0){
			plength = plength + 1;
		}
		if(page == plength){
			active = "active";
		}
		else{
			active = "";
		}
		if(plength>0){
			liTag += `<li class="numb ${active}" onclick="createPagination(${totalPages}, ${plength},${rowsPerView})"><span>${plength}</span></li>`;
		}
	}

	if(page < totalPages - 1){
		if(page < totalPages - 2){
			liTag += `<li class="dots"><span>...</span></li>`;
		}
		// liTag += `<li class="last numb" onclick="createPagination(${totalPages}, ${totalPages})"><span>${totalPages}</span></li>`;
	}

	if(page < totalPages){
		liTag += `<li class="btn next" onclick="createPagination(${totalPages}, ${page + 1},${rowsPerView})"><span>Next <i class="fas fa-angle-right"></i></span></li>`;
	}
	element.innerHTML = liTag;
	paginate(rowsPerView,page);
	return liTag;
}

function openMiniWindow(button_id){
	let url = document.getElementById(button_id).getAttribute('url');
	window.open(url, "windowname1","width=500, height=500");
	return false;
}

function openSemiWindow(button_id){
	let url = document.getElementById(button_id).getAttribute('url');
	window.open(url, "windowname1","width=900, height=500");
	return false;
}

function fill_drug_price(drug_field_id,price_field_id){
	let price  = 0;
	let drug_field = document.getElementById(drug_field_id);
	let selected_drug = drug_field.value;
	drug_field.querySelectorAll('option').forEach(opt=>{
		if(opt.getAttribute('value')==selected_drug){
			price = opt.getAttribute('price');
		}
	});
	document.getElementById(price_field_id).value=price;
}
function fill_drug_qty(drug_field_id,qty_field_id){
	let qty  = 0;
	let drug_field = document.getElementById(drug_field_id);
	let selected_drug = drug_field.value;
	drug_field.querySelectorAll('option').forEach(opt=>{
		if(opt.getAttribute('value')==selected_drug){
			qty = opt.getAttribute('qty');
		}
	});
	document.getElementById(qty_field_id).value=qty;
}
function checkValue(event) {
	let filterValue = event.target.value;
	if (filterValue) {
		filterValue = filterValue.toLowerCase();
	}
	if (event.key === 'Escape') {
		filterValue = '';
		event.target.value = ''; // clear input
	}
	let matches = false;
	for (const o of options) {
		let displayValue = '';
		if (filterValue) {
			if (o.title.toLowerCase().indexOf(filterValue) === -1) {
				displayValue = 'none';
			} else {
				matches = true;
			}
		}
		// show/hide parent <TR>
		o.node.parentNode.parentNode.style.display = displayValue;
	}
	if (!filterValue || matches) {
		event.target.classList.remove('no-results');
	} else {
		event.target.classList.add('no-results');
	}
	sessionStorage.setItem('django.admin.navSidebarFilterValue', filterValue);
}

function alertMessage(message,tag){
	Swal.fire({
		title: tag+'!',
		text: message,
		icon: tag,
		confirmButtonText: 'Ok'
	});
}
const makeToast=(icon,title)=>{
	const Toast = Swal.mixin({
		toast: true,
		position: 'top-end',
		showConfirmButton: false,
		timer: 3000,
		timerProgressBar: true,
		didOpen: (toast) => {
		  toast.addEventListener('mouseenter', Swal.stopTimer)
		  toast.addEventListener('mouseleave', Swal.resumeTimer)
		}
	  })
	  
	  Toast.fire({
		icon: icon,
		title: title
	  });
}
function makeTimerToast(){
	let timerInterval
	Swal.fire({
	title: 'Auto close alert!',
	html: 'I will close in <b></b> milliseconds.',
	timer: 2000,
	timerProgressBar: true,
	didOpen: () => {
		Swal.showLoading()
		const b = Swal.getHtmlContainer().querySelector('b')
		timerInterval = setInterval(() => {
		b.textContent = Swal.getTimerLeft()
		}, 100)
	},
	willClose: () => {
		clearInterval(timerInterval)
	}
	}).then((result) => {
	/* Read more about handling dismissals below */
	if (result.dismiss === Swal.DismissReason.timer) {
		console.log('I was closed by the timer')
	}
	})
}
function makeConfirmationToast(){
	const swalWithBootstrapButtons = Swal.mixin({
		customClass: {
		  confirmButton: 'btn btn-success',
		  cancelButton: 'btn btn-danger'
		},
		buttonsStyling: true
	  })
	  
	  swalWithBootstrapButtons.fire({
		title: 'Are you sure?',
		text: "You won't be able to revert this!",
		icon: 'warning',
		showCancelButton: true,
		confirmButtonText: 'Yes, delete it!',
		cancelButtonText: 'No, cancel!',
		reverseButtons: true
	  }).then((result) => {
		if (result.isConfirmed) {
		  swalWithBootstrapButtons.fire(
			'Deleted!',
			'Your file has been deleted.',
			'success'
		  )
		} else if (
		  /* Read more about handling dismissals below */
		  result.dismiss === Swal.DismissReason.cancel
		) {
		  swalWithBootstrapButtons.fire(
			'Cancelled',
			'Your imaginary file is safe :)',
			'error'
		  )
		}
	  })
}
window.addEventListener('load',()=>{
	if (document.querySelectorAll('.backend-message')){
		let messages = document.querySelectorAll('.backend-message');
		messages.forEach(m=>{
			let message=m.getAttribute('message_text');
			let tags=m.getAttribute('message_tags');
			// alertMessage(message,tags);
			makeToast(tags,message);
		});
	}
});

