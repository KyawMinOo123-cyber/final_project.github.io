document.addEventListener('DOMContentLoaded',function(){
    const servicePage = document.querySelector('#services_page')
    const backgroundDiv = document.querySelector('#background-div')
    const employeesPage = document.querySelector('#employee-title')
    const aboutPage = document.querySelector('#about-page')
    const careerPage = document.querySelector('#career-page')
    const navigationBar = document.querySelector('#navigation-bar')
    const updateButton = document.querySelector('#updateBtn')

   if(servicePage){
    const serviceDiv = document.querySelector('#services-div')

    backgroundDiv.innerHTML = ''
    document.body.style.backgroundColor = 'rgba(0,0,0,0.8)'

    const collapseButton = document.querySelector('#collapseButton')
    if(collapseButton){
        collapseButton.addEventListener('click',function(){
            if(collapseButton.classList.contains('clicked')){
                collapseButton.classList.remove('clicked')
                collapseButton.textContent = "Create New Service"
            }else{
                collapseButton.classList.add('clicked')
                collapseButton.textContent = "Cancel"
            }
        })
    }

    const deleteButtons = document.querySelectorAll('button')
    if(deleteButtons){
       deleteButtons.forEach(button =>{
        button.addEventListener('click', function(){
            const id = button.getAttribute('data-service-id')
            console.log(id)

            fetch('/all_services/'+id,{
                method:'POST',
                credentials:'same-origin',
                headers:{
                    'X-CSRFToken': getToken('csrftoken'),
                    'Content-Type': 'application/json'
                },
            })
            .then(res => {
                console.log('Service deleted successfully! ')
                window.location.reload()
            })
           
        });
       });
    };

    const infoButton = document.querySelectorAll('p')
    if(infoButton){
       infoButton.forEach(button => {
        button.addEventListener('click',function(){
            const id = button.getAttribute('data-info-id')
            fetch('all_services/'+id)
            .then(res => res.json())
            .then(service => {
                console.log(service)
                const serviceDivParent = document.querySelector('#service-div-parent')
                const newDiv = document.createElement('div')
                newDiv.classList.add('card','col','col-md-8')

                serviceDiv.style = `display:none;`
                
                newDiv.innerHTML = `
                    <div class="card-title"> <h1>${service.title} </h1> </div>
                    <img src="${service.image}" alt="${service.title}" >
                    <div class="card-body" > ${service.description} </div>
                    <div class="card-footer" > <a class="btn btn-primary" id="back${service.id}" >Back</a> </div>
                `
               
                serviceDivParent.append(newDiv)
                
                const backButton = document.querySelector(`#back${service.id}`)
                if(backButton){
                    backButton.addEventListener('click',function(){
                        serviceDiv.removeAttribute('style')
                        if(window.innerWidth <= 500){
                            serviceDiv.style = `
                            display: grid;
                            justify-content: center;
                            grid-template-columns: 1fr;
                            gap: 100px;
                            `
                        }else{
                            serviceDiv.style=`
                            display: grid;
                            justify-content: center;
                            grid-template-columns: 1fr 1fr 1fr;
                            gap: 100px;
                            `
                        }
                      
                        serviceDivParent.removeChild(newDiv)
                    });
                };
            });
        });
       });
    };
   };

   if(employeesPage){
    const managementBody = document.querySelector('#management-body')
    
    backgroundDiv.innerHTML = ''
    document.body.style.backgroundColor = '#fff'
    navigationBar.style.backgroundColor = "black"
   }


   if(aboutPage){
    backgroundDiv.innerHTML = '';
    navigationBar.style.backgroundColor = "black"
   }


   if(careerPage){
    const editButtons = document.querySelectorAll('.edit-button')
    const deleteCareerButtons = document.querySelectorAll('.delete-button') 
    
    backgroundDiv.innerHTML = '';
    navigationBar.style.backgroundColor = "black"
    const collapseCareerButton = document.querySelector('#collapseCareerButton')
    const careerInfo = document.querySelectorAll('p')
    const noCareer = document.querySelector('#no-career')
    
    collapseCareerButton.addEventListener('click',function(){
        if(collapseCareerButton.classList.contains('click')){
            collapseCareerButton.classList.remove('click')
            collapseCareerButton.textContent = "Create New Career"
            document.getElementById('id_title').value =""
            document.getElementById('description').value = ""
            if(noCareer){
                noCareer.style.display = "block"
            }
        }else{
            collapseCareerButton.classList.add('click')
            collapseCareerButton.textContent = "Cancel"
            if(noCareer){
                noCareer.style.display = "none"
            }
        }
    })

    careerInfo.forEach(button => button.addEventListener('click', function (){
        if(button.classList.contains('click')){
            button.classList.remove('click')
            button.textContent = "i"
        }else{
            button.classList.add('click')
            button.textContent = "^"
        }
    }));
    
    editButtons.forEach(button => button.addEventListener('click',function(){
        const id = this.getAttribute('data-edit-id')
        const content = document.getElementById(id).value
    }))

    deleteCareerButtons.forEach(button => button.addEventListener('click', function (){
        const careerDeleteId = this.getAttribute('data-delete-id')
        fetch('all_careers/'+careerDeleteId,{
            method:"POST",
            credentials:"same-origin",
            headers:{
                "X-CSRFToken":getToken('csrftoken'),
                "Content-Type":'application/json'
            }
        })
        .then(res => {
            console.log('Career Deleted Successfully')
            window.location.reload()
        })
        
    }))

    };

    if(updateButton){
        updateButton.addEventListener('click',function(){
            const id = this.getAttribute('data-update-id')
            const description = document.getElementById(id).value
            fetch('/update_description/'+id,{
                method:"POST",
                credentials:'same-origin',
                headers:{
                    'X-CSRFToken': getToken('csrftoken'),
                    'Content-Type': 'application/json'
                },
                body:JSON.stringify({
                    'description':description
                })
            })
            .then(res=>{
                return res.json()
            })
            .then(data=>{
                window.location.href = '/career'
                console.log(data.updated_career.job_description)
                document.getElementById(id).value = data.updated_career.job_description
            })
        })
       }
});



function getToken(name) {
   var cookieValue = null;
   if (document.cookie && document.cookie !== '') {
       var cookies = document.cookie.split(';');
       for (var i = 0; i < cookies.length; i++) {
           var cookie = cookies[i].trim();
           if (cookie.substring(0, name.length + 1) === (name + '=')) {
               cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
               break;
           }
       }
   }
   return cookieValue;
}