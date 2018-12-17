import autobahn from 'autobahn';

import ActionTypes from '../../constants/actionTypes';
import config from '../../config.json';
import {store} from '../../store';

const connectionInitiated = () => ({
  type: ActionTypes.WAMP_CONNECTION_INITIATED
});

const connectionSuccessful = session => ({
  type: ActionTypes.WAMP_CONNECTION_SUCCESS,
  session
});

const wampError = message => ({
  type: ActionTypes.WAMP_ERROR,
  message
});

// const subscribed = topic => ({
//     type: ActionTypes.WAMP_SUBSCRIPTION_SUCCESS,
//     topic
// });

export const connectToWAMP = () => (dispatch, getState) => {
  // if already connected, skip for now
  // it could dispatch event as warning about informing about this attempt
  if (getState().wampConnection.connected) return;

  dispatch(connectionInitiated());

  const URL = `ws://${config.crossbar.host}:${config.crossbar.port}/ws`;

  // Moze byc const?
  let wampConnection = new autobahn.Connection({
    url: URL,
    realm: config.crossbar.realm
    //   authmethods: ['wampcra'],
    //   authid: config.analytics.auth.username,
    //   onchallenge: this.onChallenge
  });

  wampConnection.onopen = session => {
    dispatch(connectionSuccessful(session));
  };

  wampConnection.open();
};

export const waitForWampReady = (callbackWhenReady) => {
    if (!store.getState().wampConnection.connected) {
        setTimeout(
            () => waitForWampReady(callbackWhenReady),
            500
        );
    }
    else
        return callbackWhenReady();
};

export const callRPC = (endpoint, args) => {
    if (!store.getState().wampConnection.connected) {
        return store.dispatch(wampError('Connection not ready yet! Use waitForWampReady method'));
    }

    return store.getState().wampConnection.session.call(endpoint, args);
};

export const subscribe = (topic, handler) => {
  // Operating on store makes it possible to avoid additional args
  // if (!store.getState().wampConnection.connected) {
  //   // For now repeat this call every 0.5 [s] infinitely
  //   // This should be changed to contain some sort of a timeout
  //   return setTimeout(
  //       () => subscribe(topic, handler),
  //       1000
  //   );
  // }
    if (!store.getState().wampConnection.connected) {
        return store.dispatch(wampError('Connection not ready yet! Use waitForWampReady method'));
    }

    return store.getState().wampConnection.session.subscribe(topic, handler);
};
