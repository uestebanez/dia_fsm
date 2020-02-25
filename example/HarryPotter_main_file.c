#include "HarryPotter.fsm"
#include "pl_mutex.h"

/*************** test object declaration ************/
typedef struct
{
    pl_mutex_t mutex;
    HarryPotter_fsm_t fsm;
    fsm_api_t api;
} fsm_test_t;

/************************* *.fsm function definitions *************************/
/* Transition actions */
static void HarryPotter_celebrate_action(HarryPotter_fsm_t* fsm)
{
    printf("\n\t\tCelebrating!!!\n\n");
}

/* Transition guard actions */
static bool HarryPotter_voldemort_condition(HarryPotter_fsm_t* fsm)
{
    char option;
    printf("\n\t\tIs it Voldemort?\n");

    fflush(stdin);
    option = getchar();

    if (option == 'y'){
        return true;
    } else if (option == 'n')
    {
        return false;
    }
}

/* Entry actions */
static void HarryPotter_put_invisibility_cloak_on_action(HarryPotter_fsm_t* fsm)
{
    printf("\n\n\t\tPutting invisibility cloak on!\n");
}

/* Do actions */
static void HarryPotter_conjure_spells_action(HarryPotter_fsm_t* fsm)
{
    printf("\n\n\t\tConjuring spells!\n");
}

static bool HarryPotter_conjure_spells_action_able(HarryPotter_fsm_t* fsm)
{
    return true;
}

static void HarryPotter_recover_healthpoints_action(HarryPotter_fsm_t* fsm)
{
    printf("\n\n\t\tRecovering healthpoints!\n");
}

static bool HarryPotter_recover_healthpoints_action_able(HarryPotter_fsm_t* fsm)
{
    return true;
}

static void HarryPotter_run_action(HarryPotter_fsm_t* fsm)
{
    printf("\n\t\tRunning!\n");
}

static bool HarryPotter_run_action_able(HarryPotter_fsm_t* fsm)
{
    return true;
}

/* Exit actions */
static void HarryPotter_take_wand_action(HarryPotter_fsm_t* fsm)
{
    printf("\n\n\t\tTaking wand!\n\n");
}

/************************* HarryPotter test functions *********************************/
void test_mutex_lock(void* user_data)
{
    fsm_test_t* test_user_data = (fsm_test_t*)user_data;
    pl_mutex_lock(&test_user_data->mutex, NULL);
}

void test_mutex_unlock(void* user_data)
{
    fsm_test_t* test_user_data = (fsm_test_t*)user_data;
    pl_mutex_unlock(&test_user_data->mutex);
}

void test_debug(void* user_data)
{
    fsm_test_t* test_user_data = (fsm_test_t*)user_data;
    printf("state change from: %s to: %s",HarryPotter_state2txt(test_user_data->fsm.previous_state),HarryPotter_state2txt(test_user_data->fsm.current_state));
}

/************************* Threading routines *********************************/
void* fsm_routine(void* arg)
{
    fsm_test_t* fsm_test = (fsm_test_t*)arg;

    /* Defining API object */
    fsm_test->api.fsm_log_state_change_fn = test_debug;
    fsm_test->api.fsm_mutex_lock_fn = test_mutex_lock;
    fsm_test->api.fsm_mutex_unlock_fn = test_mutex_unlock;

    /* Initializing mutex */
    pl_mutex_create(&fsm_test->mutex);

    /* Initializing FSM */
    HarryPotter_fsm_init(&fsm_test->fsm, &fsm_test->api, (void*)fsm_test);

    /* FSM main routine thread */
    while (1){
        HarryPotter_fsm_tick(&fsm_test->fsm);
        /* Not to collapse terminal */
        sleep(1);
    }
}

void* fsm_option_menu(void* arg)
{
    char option;
    bool skip = false;
    fsm_test_t* fsm_test = (fsm_test_t*)arg;
    
    /* Option menu thread */
    while (1){
        if (skip == false){
            printf("\nChoose your option:\n");
            printf("\t1: HarryPotter_fire_death_eater_appears_event\n");
            printf("\t2: HarryPotter_fire_beaten_death_eater_event\n");
            printf("\t3: HarryPotter_fire_healthpoints_low_event\n");
            printf("\t4: HarryPotter_fire_death_eater_dissapears_event\n\n");
        }
        /* Check if any keyboard key has been hit */
        if (_kbhit()) {
            fflush(stdin);
            option = getchar();
            skip = false;
        }
        else {
            sleep(1);
            skip = true;
            continue;
        }

        /* Firing events */
        switch (option)
        {
            case '1':
                HarryPotter_fire_death_eater_appears_event(&fsm_test->fsm);
                break;
            case '2':
                HarryPotter_fire_beaten_death_eater_event(&fsm_test->fsm);
                break;
            case '3':
                HarryPotter_fire_healthpoints_low_event(&fsm_test->fsm);
                break;
            case '4':
                HarryPotter_fire_death_eater_dissapears_event(&fsm_test->fsm);
                break;

            default:
                printf("Please choose another option");
                break;
        }
    }
}

/************************* Main function **************************************/
void main()
{
    /* Instantiating fsm test object */
    fsm_test_t fsm_test;

    printf("Let the game begin!\n");

    pl_thread_t fsm_thread[2];
    /* Creating threads */
    pl_thread_create(&fsm_thread[0], fsm_routine, (void*)&fsm_test);
    pl_thread_create(&fsm_thread[1], fsm_option_menu, (void*)&fsm_test);

    void* ret1;
    void* ret2;
    pl_thread_join(&fsm_thread[0], &ret1);
    pl_thread_join(&fsm_thread[1], &ret2);        
}