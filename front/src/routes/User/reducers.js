import {
  FETCH_GOODS_INFO_SUCCESS, FETCH_GOODS_INFO_FAILURE, FETCH_GOODS_INFO_ERROR,
  FETCH_GOODS_USERS_SUCCESS, FETCH_GOODS_USERS_FAILURE, FETCH_GOODS_USERS_ERROR
} from './actions'


// ------------------------------------
// Reducer
// ------------------------------------

function goodsInfoReducer(state = {}, action) {
  switch (action.type) {
    case FETCH_GOODS_INFO_SUCCESS:
      return action.goodsInfo
    case FETCH_GOODS_INFO_FAILURE:
    case FETCH_GOODS_INFO_ERROR:
    default:
      return state
  }
}

function goodsUsersReducer(state=[], action){
  return [...state, ...action.goodsUsers]
}

const initialState = {}
export default function goodsDetailReducer(state = initialState, action) {
  switch (action.type) {
    case FETCH_GOODS_INFO_SUCCESS:
    case FETCH_GOODS_INFO_FAILURE:
    case FETCH_GOODS_INFO_ERROR:
      return {
        ...state,
        goodsInfo: goodsInfoReducer(state.goodsInfo = {}, action)
      }

    case FETCH_GOODS_USERS_SUCCESS:
    case FETCH_GOODS_USERS_FAILURE:
    case FETCH_GOODS_USERS_ERROR:
      return {
        ...state,
        goodsUsers: goodsUsersReducer(state.goodsUsers = [], action)
      }
    default:
      return state
  }
}




