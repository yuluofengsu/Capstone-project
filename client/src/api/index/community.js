import axios from '@/utils/request'

// 帖子相关
export const listPost = (params) => {
    return axios({
        url: '/myapp/index/community/post/list',
        method: 'get',
        params: params
    })
}

export const createPost = (data) => {
    return axios({
        url: '/myapp/index/community/post/create',
        method: 'post',
        data: data
    })
}

export const detailPost = (params) => {
    return axios({
        url: '/myapp/index/community/post/detail',
        method: 'get',
        params: params
    })
}

export const likePost = (params) => {
    return axios({
        url: '/myapp/index/community/post/like',
        method: 'post',
        params: params
    })
}

export const deletePost = (params) => {
    return axios({
        url: '/myapp/index/community/post/delete',
        method: 'post',
        params: params
    })
}

// 活动相关
export const listEvent = (params) => {
    return axios({
        url: '/myapp/index/community/event/list',
        method: 'get',
        params: params
    })
}

export const detailEvent = (params) => {
    return axios({
        url: '/myapp/index/community/event/detail',
        method: 'get',
        params: params
    })
}

// 评论相关
export const listComment = (params) => {
    return axios({
        url: '/myapp/index/community/comment/list',
        method: 'get',
        params: params
    })
}

export const createComment = (data) => {
    return axios({
        url: '/myapp/index/community/comment/create',
        method: 'post',
        data: data
    })
}

export const deleteComment = (params) => {
    return axios({
        url: '/myapp/index/community/comment/delete',
        method: 'post',
        params: params
    })
}
