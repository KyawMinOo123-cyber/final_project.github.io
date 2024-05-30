document.addEventListener('DOMContentLoaded',function() {
    const servicePage = document.querySelector('#services_page')
    const backgroundDiv = document.querySelector('#background-div')
    const employeesPage = document.querySelector('#employee-title')
    const aboutPage = document.querySelector('#about-page')
    const careerPage = document.querySelector('#career-page')
    const navigationBar = document.querySelector('#navigation-bar')
    const updateButton = document.querySelector('#updateBtn')
    const jobApplyForm = document.querySelector('#job-apply-form')
    const allApplications = document.querySelector('#all-applications-div')
    const body = document.getElementById('bodyId')

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
}

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
    
    if(collapseCareerButton){
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
    }

    if(careerInfo){
        careerInfo.forEach(button => button.addEventListener('click',()=>{
            if(button.classList.contains('click')){
                button.classList.remove('click')
                button.textContent = "i"
                console.log("i")
            }else{
                button.classList.add('click')
                button.textContent = "^"
                console.log('^')
            }
        }));
    }
    
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

    if(jobApplyForm){
        backgroundDiv.innerHTML = ''
        document.body.style.backgroundColor = 'rgba(0,0,0,0.8)'
        navigationBar.style.backgroundColor = "black"
    }

    const application_info_div = document.createElement('div')
    body.append(application_info_div)
    application_info_div.style =`
        display:none;
    `
    const newEmployeeForm = document.createElement('div')
    body.append(newEmployeeForm)
    newEmployeeForm.style  = `
        display:none;
    `

    if(allApplications){ 

        backgroundDiv.innerHTML = ''
        document.body.style.backgroundColor = `rgba(0,0,0,0.8)`

        const allApplicationDiv = document.querySelectorAll('.all-applications')

        if(allApplicationDiv){

            allApplicationDiv.forEach(application => {
                application.addEventListener('click' , function (){
                    
                    allApplications.style = `
                     display:none !important;
                    `

                    application_info_div.style = `
                        display:block;
                        padding:20px;
                        `

                    const id = this.getAttribute('data-application-id')

                    fetch('new_application_info/'+id)
                    .then(res=> res.json())
                    .then(application => {
                        application_info_div.innerHTML = `
                        <div class="d-flex justify-content-center">     
                            <div class='card col-12 col-md-3 p-3'>
                            <h5 class="text-start">Name: ${application.job_applier}</h5>
                            <h5 class="text-start">Position: ${application.position}</h5>
                            <h5 class="text-start">Expected Salary:<spam class="text-primary"> ${application.expected_salary}</spam></h5>
                            <h5 class="text-start">Contact Number: ${application.contact_number}</h5>
                            <h5 class="text-start">Cover Letter<br> ${application.cover_letter}</h5>
                            <h5 class="text-start">Date Applied: ${application.timestamp}</h5>
                            <div id="footer" class="card-footer d-flex justify-content-between align-items-center"> 
                            </div>
                            <button class="back-button" class="rounded">Back</button>
                            </div>
                        </div>
                        `
                        const footerDiv  = document.getElementById('footer')
                        if(footerDiv){
                            if(application.interview){
                                footerDiv.innerHTML = `
                                    <button id="hire" data-hire-id=${application.id} class="btn btn-primary">Hire</button>
                                    <button id="reject${application.id}" data-reject-id=${application.id} class="btn btn-danger">Reject</button>
                                `
                            }else{
                                footerDiv.innerHTML = `
                                    <button id="interview${application.id}" data-interview-id=${application.id} class="btn btn-primary">Interview</button>
                                    <button id="reject${application.id}" data-reject-id=${application.id} class="btn btn-danger">Reject</button>
                                `
                            }
                        }

                        const hireButton = document.querySelector('#hire')
                        if(hireButton){
                            hireButton.addEventListener('click',function(){
                                const id = this.getAttribute('data-hire-id')
                                fetch('employee_hiring_form/'+id)
                                .then(res => res.json())
                                .then(application => {
                                    console.log(application)
                                    application_info_div.style = `
                                        display:none; 
                                    `
                                    
                                    newEmployeeForm.innerHTML = `
                                        <h3 class="text-center text-warning mb-2">New Employee Detail Form</h3>

                                        <label class="text-light" for="apply_user"></label>
                                        <input id="apply_user" name="user" class="form-control mb-3" type="text" value = "${application.applying_user}" required> 

                                        <label class="text-light" for="applier_name">Name</label>
                                        <input id="applier_name" name="name" class="form-control mb-3" type="text" value ="${application.job_applier}" required>

                                        <label class="text-light" for="applier_position">Position</label>
                                        <input id="applier_position" type="text" value="${application.position}" class="form-control" required>

                                        <label class="text-light" for="applier_expected_salary">Salary</label>
                                        <input id="applier_expected_salary" type="text" class="form-control" required>

                                        <label class="text-light" for="applier_contact_number">Contact Number</label>
                                        <input type="text" id="applier_contact_number" value="${application.contact_number}" class="form-control" required>

                                        <label class="text-light" for="applier_gender">Gender</label>
                                        <input type="text" id="applier_gender" class="form-control" required>

                                        <label class="text-light" for="applier_department">Department</label>
                                        <input type="text" id="applier_department" class="form-control" required>
        
                                        <div class=" mt-3 d-flex justify-content-between align-items-center">
                                            <button id="saveButton" data-save-id=${application.id} class="btn btn-primary">Save</button> 
                                            <button id="cancelButton" class="btn btn-danger">Cancel</a> 
                                        </div>
                                    `

                                    newEmployeeForm.style = `
                                        display:block;
                                        padding:50px;
                                        height:100vh;
                                        width:100vw;
                                    `

                                    const cancelButton = document.querySelector('#cancelButton')
                                    if(cancelButton){
                                        cancelButton.addEventListener('click',function(){
                                            console.log('clicked')
                                            newEmployeeForm.style = `display:none;`
                                            application_info_div.style = `display:block;`
                                        })
                                    }

                                    const saveButton = document.querySelector('#saveButton')
                                    if(saveButton){
                                        saveButton.addEventListener('click',function(){
                                            const id = this.getAttribute('data-save-id')
                                            console.log(id)
                                        })
                                    }
                                
                                })
                            })}
                        
                        const backButton = document.querySelector('.back-button')
                            backButton.addEventListener('click',function(){
                                application_info_div.style = `display:none !important;`
                                allApplications.style = `display:flex !important;`
                                allApplications.classList.add('p-5','border')
                            })
                        
                        const rejectButton = document.getElementById(`reject${application.id}`)
                        rejectButton.addEventListener('click',function(){
                            const id = this.getAttribute('data-reject-id')
                            fetch('rejected_application/'+id)
                            .then(res => res.json())
                            .then(data => {
                                if(data.success){
                                    console.log(data)
                                    application_info_div.style = `display:none !important;`
                                    allApplications.style = `display:flex !important;`
                                    allApplications.classList.add('p-5','border')
                                    window.location.reload()
                                }
                                else{
                                    console.log(data)
                                    const errorDiv = document.createElement('div')
                                    errorDiv.innerHtml = `
                                     <h3 class="text-center text-danger">${data.error}</h3>
                                    `
                                }
                            })
                        })

                        //to add new applications to interview list
                        const interviewButton = document.getElementById(`interview${application.id}`)
                        if(interviewButton){
                            interviewButton.addEventListener('click',function(){
                                const id = this.getAttribute('data-interview-id')
                                
                                fetch('add_to_interview/'+id)
                                .then(res => res.json())
                                .then(data =>{
                                    console.log(data)
                                    application_info_div.style = `display:none !important;`
                                    allApplications.style = `display:flex !important;`
                                    allApplications.classList.add('p-5','border')
                                    window.location.reload()
                                }) 
                            })
                        }

                    })
                })
            })
        }
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