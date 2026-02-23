import axios from '@/utils/request'

export const listApi = (params) => {
  return axios({
    url: '/myapp/admin/event/list',
    method: 'get',
    params: params
  })
}

export const createApi = (data) => {
  return axios({
    url: '/myapp/admin/event/create',
    method: 'post',
    data: data,
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
}

export const updateApi = (params, data) => {
  return axios({
    url: '/myapp/admin/event/update',
    method: 'post',
    data: data,
    params: params,
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
}

export const deleteApi = (params) => {
  return axios({
    url: '/myapp/admin/event/delete',
    method: 'post',
    params: params
  })
}
