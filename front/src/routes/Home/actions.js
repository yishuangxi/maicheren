/**
 * Created by Yi on 13/10/2016.
 */
import fetch from 'isomorphic-fetch'
import {ifFetchFailure, fetchError} from '../Common/error'

export const FETCH_GOODS_LIST = 'FETCH_GOODS_LIST'
export const FETCH_GOODS_LIST_SUCCESS = 'FETCH_GOODS_LIST_SUCCESS'
export const FETCH_GOODS_LIST_FAILURE = 'FETCH_GOODS_LIST_FAILURE'
export const FETCH_GOODS_LIST_ERROR = 'FETCH_GOODS_LIST_ERROR'

export const FETCH_BANNER_LIST_SUCCESS = 'FETCH_BANNER_LIST_SUCCESS'
export const FETCH_BANNER_LIST_FAILURE = 'FETCH_BANNER_LIST_FAILURE'
export const FETCH_BANNER_LIST_ERROR = 'FETCH_BANNER_LIST_ERROR'

export const FETCH_MSG_LIST_SUCCESS = 'FETCH_MSG_LIST_SUCCESS'
export const FETCH_MSG_LIST_FAILURE = 'FETCH_MSG_LIST_FAILURE'
export const FETCH_MSG_LIST_ERROR = 'FETCH_MSG_LIST_ERROR'

export function fetchGoodsList() {
  return (dispatch, getState) => {
    return fetch(`/api/issue/list`)
      .then(response => response.json())
      .then(json => ifFetchFailure(json, dispatch, fetchGoodsListFailure))
      .then(json => dispatch(fetchGoodsListSuccess(json.data.items)))
      .catch(err => fetchError(err, dispatch, fetchGoodsListError))
  }
}


export function fetchGoodsListSuccess(goodsList) {
  return {
    type: FETCH_GOODS_LIST_SUCCESS,
    goodsList: goodsList,
    time: Date.now()
  }
}

export function fetchGoodsListFailure() {
  return {
    type: FETCH_GOODS_LIST_FAILURE,
    goodsList: []
  }
}

export function fetchGoodsListError() {
  return {
    type: FETCH_GOODS_LIST_ERROR,
    goodsList: []
  }
}


export function fetchBannerList() {
  return (dispatch, getState) => {
    return fetch(`/api/banner`)
      .then(response => response.json())
      .then(json => ifFetchFailure(json, dispatch, fetchBannerListFailure))
      .then(json => dispatch(fetchBannerListSuccess(json.data)))
      .catch(err => fetchError(err, dispatch, fetchBannerListError))
  }
}

export function fetchBannerListSuccess(bannerList) {
  return {
    type: FETCH_BANNER_LIST_SUCCESS,
    bannerList: bannerList,
    time: Date.now()
  }
}

export function fetchBannerListFailure() {
  return {
    type: FETCH_BANNER_LIST_FAILURE,
    bannerList: []
  }
}

export function fetchBannerListError() {
  return {
    type: FETCH_BANNER_LIST_ERROR,
    bannerList: []
  }
}

export function fetchMsgList() {
  return (dispatch, getState) => {
    return fetch(`/api/msg/notice`)
      .then(response => response.json())
      .then(json => ifFetchFailure(json, dispatch, fetchMsgListFailure))
      .then(json => dispatch(fetchMsgListSuccess(json.messages)))
      .catch(err => fetchError(err, dispatch, fetchMsgListError))
  }
}

export function fetchMsgListSuccess(msgList) {
  return {
    type: FETCH_MSG_LIST_SUCCESS,
    msgList: msgList,
    time: Date.now()
  }
}

export function fetchMsgListFailure() {
  return {
    type: FETCH_MSG_LIST_FAILURE,
    msgList: []
  }
}

export function fetchMsgListError() {
  return {
    type: FETCH_MSG_LIST_ERROR,
    msgList: []
  }
}
