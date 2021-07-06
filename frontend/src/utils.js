export const getLocalToken = () => localStorage.getItem("token")
export const setLocalToken = (token) => localStorage.setItem("token", token)
export const removeLocalToken = () => localStorage.removeItem("token")