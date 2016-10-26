/**
 * Created by Yi on 13/10/2016.
 */
import fetch from 'isomorphic-fetch'
import {ifFetchFailure, fetchError} from '../Common/error'

export const FETCH_GOODS_INFO_SUCCESS = 'FETCH_GOODS_INFO_SUCCESS'
export const FETCH_GOODS_INFO_FAILURE = 'FETCH_GOODS_INFO_FAILURE'
export const FETCH_GOODS_INFO_ERROR = 'FETCH_GOODS_INFO_ERROR'

export const FETCH_GOODS_USERS_SUCCESS = 'FETCH_GOODS_USERS_SUCCESS'
export const FETCH_GOODS_USERS_FAILURE = 'FETCH_GOODS_USERS_FAILURE'
export const FETCH_GOODS_USERS_ERROR = 'FETCH_GOODS_USERS_ERROR'


export function fetchGoodsInfo(id) {
  return (dispatch, getState) => {
    return fetch(`/api/issue/${id}`)
      .then(response => response.json())
      .then(json => ifFetchFailure(json, dispatch, fetchGoodsInfoFailure()))
      .then(json => dispatch(fetchGoodsInfoSuccess(json.data)))
      .catch(err => fetchError(err, dispatch, fetchGoodsInfoError()))
  }
}

export function fetchGoodsInfoSuccess(goodsInfo) {
  return {
    type: FETCH_GOODS_INFO_SUCCESS,
    goodsInfo: goodsInfo,
    time: Date.now()
  }
}

export function fetchGoodsInfoFailure() {
  return {
    type: FETCH_GOODS_INFO_FAILURE
  }
}

export function fetchGoodsInfoError() {
  return {
    type: FETCH_GOODS_INFO_ERROR
  }
}

export function fetchGoodsUsers(id) {
  return (dispatch, getState) => {
    return fetch(`/api/issue/${id}`)
      .then(response => response.json())
      .then(json => ifFetchFailure(json, dispatch, fetchGoodsUsersFailure()))
      .then(json => dispatch(fetchGoodsUsersSuccess(json.data)))
      .catch(err => fetchError(err, dispatch, fetchGoodsUsersError()))
  }
}

export function fetchGoodsUsersSuccess(goodsUsers) {
  return {
    type: FETCH_GOODS_USERS_SUCCESS,
    goodsUsers: goodsUsers,
    time: Date.now()
  }
}

export function fetchGoodsUsersFailure() {
  return {
    type: FETCH_GOODS_USERS_FAILURE
  }
}

export function fetchGoodsUsersError() {
  return {
    type: FETCH_GOODS_USERS_ERROR
  }
}