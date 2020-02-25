#ifndef FSM_API_H
#define FSM_API_H

#include <assert.h>
#include <stddef.h>

typedef void (*fsm_debug_t)(void* user_data);
typedef void (*fsm_mutex_lock_t)(void* user_data);
typedef void (*fsm_mutex_unlock_t)(void* user_data);

typedef struct _fsm_api_t
{
	fsm_debug_t			fsm_log_state_change_fn;
	fsm_mutex_lock_t	fsm_mutex_lock_fn;
	fsm_mutex_unlock_t	fsm_mutex_unlock_fn;
} fsm_api_t;

static inline void fsm_api_debug(fsm_api_t* api, void* user_data);
static inline void fsm_api_lock(fsm_api_t* api, void* user_data);
static inline void fsm_api_unlock(fsm_api_t* api, void* user_data);

static inline void fsm_api_debug(fsm_api_t* api, void* user_data)
{    
    assert(api != NULL);
    assert(api->fsm_log_state_change_fn != NULL);
    
    api->fsm_log_state_change_fn(user_data);
}

static inline void fsm_api_lock(fsm_api_t* api, void* user_data)
{    
    assert(api != NULL);
    assert(api->fsm_mutex_lock_fn != NULL);
    
    api->fsm_mutex_lock_fn(user_data);
}

static inline void fsm_api_unlock(fsm_api_t* api, void* user_data)
{    
    assert(api != NULL);
    assert(api->fsm_mutex_unlock_fn != NULL);
    
    api->fsm_mutex_unlock_fn(user_data);
}

#endif /* FSM_API_H */