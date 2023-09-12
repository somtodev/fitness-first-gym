const UPDATE_FORM = document.querySelector('[update-form]')


UPDATE_FORM.addEventListener('submit', handleSubmit)

function handleSubmit(event){
    event.preventDefault()

    const new_password = UPDATE_FORM.querySelector('[new-password]').value
    const conf_new_password = UPDATE_FORM.querySelector('[conf-new-password]').value
    let err_msg = UPDATE_FORM.querySelector('[err-msg]')

    if(new_password !== conf_new_password){
        err_msg.textContent = 'New Password Do Not Match'
        return
    }

    UPDATE_FORM.submit()


}
