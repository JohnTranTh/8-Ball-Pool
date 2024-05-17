#include "phylib.h"

#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>

/* Allocates memory for a still ball, transfers the parameters information, then returns the ball. Returns NULL if failed. */
phylib_object *phylib_new_still_ball( unsigned char number,
                                    phylib_coord *pos ) 
{
    phylib_object * new_still_ball;

    new_still_ball = (phylib_object *) malloc (sizeof(phylib_object));

    if (new_still_ball == NULL) 
    {
        return NULL;
    }

    new_still_ball->type = PHYLIB_STILL_BALL;
    new_still_ball->obj.still_ball.number = number;
    new_still_ball->obj.still_ball.pos = *pos;

    return new_still_ball;

}

/* Allocates memory for a rolling ball, transfers the parameters information, then returns the ball. Returns NULL if failed. */
phylib_object *phylib_new_rolling_ball( unsigned char number,
                                phylib_coord *pos,
                                phylib_coord *vel,
                                phylib_coord *acc )
{
    phylib_object * new_rolling_ball;

    new_rolling_ball = (phylib_object *) malloc (sizeof(phylib_object));
 
    if (new_rolling_ball == NULL) 
    {
        return NULL;
    }

    new_rolling_ball->type = PHYLIB_ROLLING_BALL;
    new_rolling_ball->obj.rolling_ball.number = number;
    new_rolling_ball->obj.rolling_ball.pos = *pos;
    new_rolling_ball->obj.rolling_ball.vel = *vel;
    new_rolling_ball->obj.rolling_ball.acc = *acc;

    return new_rolling_ball;
}

/* Allocates memory for a hole, transfers the parameters information, then returns the hole. Returns NULL if failed. */
phylib_object *phylib_new_hole( phylib_coord *pos )
{
    phylib_object * new_hole;

    new_hole = (phylib_object *) malloc (sizeof(phylib_object));

    if (new_hole == NULL) 
    {
        return NULL;
    }

    new_hole->type = PHYLIB_HOLE;
    new_hole->obj.hole.pos = *pos;

    return new_hole;
}

/* Allocates memory for a horizontal cushion, transfers the parameters information, then returns the cushion. Returns NULL if failed. */
phylib_object *phylib_new_hcushion( double y )
{
    phylib_object * new_hcushion;

    new_hcushion = (phylib_object *) malloc (sizeof(phylib_object));

    if (new_hcushion == NULL) 
    {
        return NULL;
    }

    new_hcushion->type = PHYLIB_HCUSHION;
    new_hcushion->obj.hcushion.y = y;  

    return new_hcushion;
}

/* Allocates memory for a vertical cushion, transfers the parameters information, then returns the cushion. Returns NULL if failed. */
phylib_object *phylib_new_vcushion( double x )
{
    phylib_object * new_vcushion;

    new_vcushion = (phylib_object *) malloc (sizeof(phylib_object));

    if (new_vcushion == NULL) 
    {
        return NULL;
    }

    new_vcushion->type = PHYLIB_VCUSHION;
    new_vcushion->obj.vcushion.x = x;  

    return new_vcushion;
}

/* Allocates memory for a table, transfers the parameters information, then returns the table. Returns NULL if failed.
The order of objects will be two horizontal cushions, two vertical cushions, then 6 holes. */
phylib_table *phylib_new_table( void )
{
    phylib_table * new_table;
    phylib_coord pos;

    new_table = (phylib_table *) malloc (sizeof(phylib_table));

    if (new_table == NULL) 
    {
        return NULL;
    }

    new_table->time = 0.0;
    new_table->object[0] = phylib_new_hcushion(0.0);
    new_table->object[1] = phylib_new_hcushion(PHYLIB_TABLE_LENGTH);
    new_table->object[2] = phylib_new_vcushion(0.0);
    new_table->object[3] = phylib_new_vcushion(PHYLIB_TABLE_WIDTH);

    pos.x = new_table->object[2]->obj.vcushion.x;
    pos.y = new_table->object[0]->obj.hcushion.y;
    new_table->object[4] = phylib_new_hole(&pos); // hole at (0,0)

    pos.y = PHYLIB_TABLE_LENGTH / 2;
    new_table->object[5] = phylib_new_hole(&pos); // (0, 1350)

    pos.y = PHYLIB_TABLE_LENGTH;
    new_table->object[6] = phylib_new_hole(&pos); // (0, 2700)

    pos.x = new_table->object[3]->obj.vcushion.x;
    pos.y = new_table->object[0]->obj.hcushion.y;
    new_table->object[7] = phylib_new_hole(&pos); // (1350, 0)

    pos.y = PHYLIB_TABLE_LENGTH / 2;
    new_table->object[8] = phylib_new_hole(&pos); // (1350, 1350)

    pos.y = PHYLIB_TABLE_LENGTH;
    new_table->object[9] = phylib_new_hole(&pos); // (1350, 2700)

    for (int i = 10; i < PHYLIB_MAX_OBJECTS; i++) 
    {
        new_table->object[i] = NULL; // Set remaining objects to null
    }

    return new_table;
}

/* Allocates memory for a phylib_object and places the address at dest. Then copies the contents from src into dest.
If src is NULL, dest is set to NULL. */
void phylib_copy_object( phylib_object **dest, phylib_object **src )
{
    phylib_object * copy_object;

// Do not malloc if null
    if (*src == NULL) 
    {
        *dest = NULL;
        return;
    }

    copy_object = (phylib_object *) malloc (sizeof(phylib_object));
    *dest = copy_object;
    memcpy(copy_object, *src, sizeof(phylib_object)); // Deep copy
}

/* Allocates memory for a table, then copies the content of the parameter into the new table and returns it. Returns NULL if failed. */
phylib_table *phylib_copy_table( phylib_table *table )
{
    phylib_table * copy_table;

    copy_table = (phylib_table *) malloc (sizeof(phylib_table));

    if (copy_table == NULL) 
    {
        return NULL;
    }

    copy_table->time = table->time;

    for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++) 
    {
        phylib_copy_object(&copy_table->object[i], &table->object[i]); // Copy objects into new table
    }

    return copy_table;
}

/* Assigns the first NULL pointer in the table's object array to the address of the passed object parameter.
The functions does nothing if a NULL pointer is not found. */
void phylib_add_object( phylib_table *table, phylib_object *object )
{
    for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++) 
    {
        if (table->object[i] == NULL) 
        {
            table->object[i] = object;
            break;
        }
    }
}

/* Frees all pointers in the object array of the table, then frees the table itself. */
void phylib_free_table( phylib_table *table )
{
    for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++) 
    {
        free(table->object[i]); // Free does nothing if the pointer is NULL
    }
    free(table);
}

/* Returns the difference between c1 and c2's x and y values as a phylib_coord. */
phylib_coord phylib_sub( phylib_coord c1, phylib_coord c2 )
{
    phylib_coord difference;

    difference.x = c1.x - c2.x;
    difference.y = c1.y - c2.y;

    return difference;
}

/* Returns the length of the vector/coordinate c. */
double phylib_length( phylib_coord c )
{
    double length;

    length = sqrt((c.x * c.x) + (c.y * c.y));

    return length;
}

/* Returns the dot product of two vectors. */
double phylib_dot_product( phylib_coord a, phylib_coord b )
{
    double dot_product;

    dot_product = ((a.x * b.x) + (a.y * b.y));

    return dot_product;
}

/* Returns the distance between two phylib_objects. If obj1 is not a rolling ball or obj2 is not a valid type,
the function returns -1.0. */
double phylib_distance( phylib_object *obj1, phylib_object *obj2 )
{
    phylib_coord difference;
    double distance;

    if (obj1->type != PHYLIB_ROLLING_BALL) 
    {
        return -1.0;
    }

    // Position assumes the coordinates are in the center of the ball. Therefore, the radius of the objects must be subtracted.
    if (obj2->type == PHYLIB_STILL_BALL) 
    {
        difference = phylib_sub(obj1->obj.rolling_ball.pos, obj2->obj.still_ball.pos);
        distance = phylib_length(difference) - PHYLIB_BALL_DIAMETER;
    }
    else if (obj2->type == PHYLIB_ROLLING_BALL) 
    {
        difference = phylib_sub(obj1->obj.rolling_ball.pos, obj2->obj.rolling_ball.pos);
        distance = phylib_length(difference) - PHYLIB_BALL_DIAMETER;
    }
    else if (obj2->type == PHYLIB_HOLE) 
    {
        difference = phylib_sub(obj1->obj.rolling_ball.pos, obj2->obj.hole.pos);
        distance = phylib_length(difference) - PHYLIB_HOLE_RADIUS;
    }
    else if (obj2->type == PHYLIB_VCUSHION) 
    {
        distance = fabs(obj1->obj.rolling_ball.pos.x - obj2->obj.vcushion.x) - PHYLIB_BALL_RADIUS; // Absolute value since ball can be left/right of cushion
    }
    else if (obj2->type == PHYLIB_HCUSHION) 
    {
        distance = fabs(obj1->obj.rolling_ball.pos.y - obj2->obj.hcushion.y) - PHYLIB_BALL_RADIUS; // Absolute value since ball can be above/below of cushion      
    }
    else 
    {
        return -1.0;
    }

    return distance;
}

/* Simulates ball rolling on table by updating the position and velocity of the ball. 
new represents the old object after it has rolled for a period of time.
If the velocities change signs, that velocity component and its acceleration is set to 0. 
If both objects are not rolling balls, the function does nothing. */
void phylib_roll( phylib_object *new, phylib_object *old, double time ) 
{
    double old_pos;
    double old_vel;
    double old_acc;
    double velocity_old;
    double velocity_new;

    if (new->type != PHYLIB_ROLLING_BALL && old->type != PHYLIB_ROLLING_BALL) 
    {
        return;
    }

    // x component of position calculations
    old_pos = old->obj.rolling_ball.pos.x;
    old_vel = old->obj.rolling_ball.vel.x;
    old_acc = old->obj.rolling_ball.acc.x;
    new->obj.rolling_ball.pos.x = old_pos + (old_vel * time) + (0.5 * old_acc * time * time);

    // y component of position calculations
    old_pos = old->obj.rolling_ball.pos.y;
    old_vel = old->obj.rolling_ball.vel.y;
    old_acc = old->obj.rolling_ball.acc.y;
    new->obj.rolling_ball.pos.y = old_pos + (old_vel * time) + (0.5 * old_acc * time * time);

    // // x component of velocity calculations
    velocity_old = old->obj.rolling_ball.vel.x;
    velocity_new = old->obj.rolling_ball.vel.x + old->obj.rolling_ball.acc.x * time;
    if ((velocity_new < 0.0 && velocity_old < 0.0) || (velocity_new >= 0.0 && velocity_old >= 0.0)) // change sign check
    {
        new->obj.rolling_ball.vel.x = velocity_new;
    }
    else 
    {
        new->obj.rolling_ball.vel.x = 0.0;
        new->obj.rolling_ball.acc.x = 0.0;
    }

    // y component of velocity calculations
    velocity_old = old->obj.rolling_ball.vel.y;
    velocity_new = old->obj.rolling_ball.vel.y + old->obj.rolling_ball.acc.y * time;
    if ((velocity_new < 0.0 && velocity_old < 0.0) || (velocity_new >= 0.0 && velocity_old >= 0.0)) // change sign check
    {
        new->obj.rolling_ball.vel.y = velocity_new;
    }
    else 
    {
        new->obj.rolling_ball.vel.y = 0.0;
        new->obj.rolling_ball.acc.y = 0.0;
    }
}

/* Checks if a rolling ball has stopped. If it has, convert it into a still ball. 
Assumes the object passed is a rolling ball. Returns 1 if it converts, 0 otherwise. */
unsigned char phylib_stopped( phylib_object *object ) 
{
    unsigned char number = object->obj.rolling_ball.number;
    phylib_coord pos = object->obj.rolling_ball.pos;
    double x = object->obj.rolling_ball.pos.x;
    double y = object->obj.rolling_ball.pos.y;

    if (phylib_length(object->obj.rolling_ball.vel) < PHYLIB_VEL_EPSILON) // Ball is stopped if speed is less than VEL_EPSILON
    {
        object->type = PHYLIB_STILL_BALL;
        object->obj.still_ball.number = number;
        object->obj.still_ball.pos = pos;
        object->obj.still_ball.pos.x = x;
        object->obj.still_ball.pos.y = y;
        return 1;
    }

    return 0;
}

/* Simulates a rolling ball bouncing off of an object. Assumes 'a' is a rolling ball. */
void phylib_bounce( phylib_object **a, phylib_object **b ) 
{
    unsigned char temp_num;
    phylib_coord temp_pos;
    phylib_coord r_ab;
    phylib_coord v_rel;
    phylib_coord n;
    double v_rel_n;
    double speed_a;
    double speed_b;
    
    switch ((*b)->type) 
    {
        // Physical principle of angle of incidence equals angle of reflection
        case PHYLIB_HCUSHION:
            (*a)->obj.rolling_ball.vel.y = (*a)->obj.rolling_ball.vel.y * -1.0;
            (*a)->obj.rolling_ball.acc.y = (*a)->obj.rolling_ball.acc.y * -1.0;
            break;

        // Physical principle of angle of incidence equals angle of reflection
        case PHYLIB_VCUSHION: 
            (*a)->obj.rolling_ball.vel.x = (*a)->obj.rolling_ball.vel.x * -1.0;
            (*a)->obj.rolling_ball.acc.x = (*a)->obj.rolling_ball.acc.x * -1.0;
            break;

        // Ball has fallen into hole
        case PHYLIB_HOLE:
            free((*a));
            *a = NULL;
            break;

        // If still ball, upgrade to rolling ball then perform rolling ball case
        case PHYLIB_STILL_BALL:
            temp_num = (*b)->obj.still_ball.number;
            temp_pos = (*b)->obj.still_ball.pos;
            (*b)->type = PHYLIB_ROLLING_BALL;
            (*b)->obj.rolling_ball.number = temp_num;
            (*b)->obj.rolling_ball.pos = temp_pos;
            (*b)->obj.rolling_ball.vel.x = 0.0;
            (*b)->obj.rolling_ball.vel.y = 0.0;
            (*b)->obj.rolling_ball.acc.x = 0.0;
            (*b)->obj.rolling_ball.acc.y = 0.0;

        // Collision of two rolling balls
        case PHYLIB_ROLLING_BALL:
            r_ab = phylib_sub((*a)->obj.rolling_ball.pos, (*b)->obj.rolling_ball.pos); // position of 'a' to 'b'
            v_rel = phylib_sub((*a)->obj.rolling_ball.vel, (*b)->obj.rolling_ball.vel); // relative velocity of 'a' to 'b'

            n.x = r_ab.x / phylib_length(r_ab); // normal vector
            n.y = r_ab.y / phylib_length(r_ab);
            v_rel_n = phylib_dot_product(v_rel, n); // Ratio of relative velocity in direction of ball 'a'

            // Ball 'a' will roll perpendicular to the direction from 'a' to 'b'
            (*a)->obj.rolling_ball.vel.x = (*a)->obj.rolling_ball.vel.x - v_rel_n * n.x;
            (*a)->obj.rolling_ball.vel.y = (*a)->obj.rolling_ball.vel.y - v_rel_n * n.y; 

            // Ball 'b' will run in the direction from 'a' to 'b'
            (*b)->obj.rolling_ball.vel.x = (*b)->obj.rolling_ball.vel.x + v_rel_n * n.x;
            (*b)->obj.rolling_ball.vel.y = (*b)->obj.rolling_ball.vel.y + v_rel_n * n.y;

            // Reverse the acceleration if needed to match the new direction the ball is travelling
            speed_a = phylib_length((*a)->obj.rolling_ball.vel);
            if (speed_a > PHYLIB_VEL_EPSILON) 
            {
                (*a)->obj.rolling_ball.acc.x = ((-1.0 * (*a)->obj.rolling_ball.vel.x) / speed_a) * PHYLIB_DRAG;
                (*a)->obj.rolling_ball.acc.y = ((-1.0 * (*a)->obj.rolling_ball.vel.y) / speed_a) * PHYLIB_DRAG;
            }
            
            speed_b = phylib_length((*b)->obj.rolling_ball.vel);
            if (speed_b > PHYLIB_VEL_EPSILON) 
            {
                (*b)->obj.rolling_ball.acc.x = ((-1.0 * (*b)->obj.rolling_ball.vel.x) / speed_b) * PHYLIB_DRAG;
                (*b)->obj.rolling_ball.acc.y = ((-1.0 * (*b)->obj.rolling_ball.vel.y) / speed_b) * PHYLIB_DRAG;
            }
            break;
    }
}

/* Returns the number of rolling balls on the table. */
unsigned char phylib_rolling( phylib_table *t ) 
{
    unsigned char rolling_balls = 0;

    for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++) 
    {
        if (t->object[i] != NULL && t->object[i]->type == PHYLIB_ROLLING_BALL) 
        {
            rolling_balls = rolling_balls + 1;
        }
    }

    return rolling_balls;
}

/* Simulates a segment of a pool shot. Returns a copied table that is the result
of performing phylib_roll on each rolling ball.
Returns NULL if there are no rolling balls on the table. */
phylib_table *phylib_segment( phylib_table *table ) 
{
    unsigned char rolling_balls = phylib_rolling(table);
    phylib_table * new_table;
    int stop = 0;
    double distance;
    int balls_bounced[PHYLIB_MAX_OBJECTS] = {0}; // Track if a rolling ball has bounced already to prevent double bouncing

    if (rolling_balls == 0) 
    {
        return NULL;
    }

    new_table = phylib_copy_table(table);

    for (double time = PHYLIB_SIM_RATE; time < PHYLIB_MAX_TIME; time += PHYLIB_SIM_RATE) 
    {
        for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++) 
        {
            if (new_table->object[i] != NULL && new_table->object[i]->type == PHYLIB_ROLLING_BALL) 
            {
                phylib_roll(new_table->object[i], table->object[i], time); // Roll each rolling ball
            }
        }
        new_table->time += PHYLIB_SIM_RATE;

        for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++) // Outer loop represents rolling ball
        {
            if (new_table->object[i] != NULL && new_table->object[i]->type == PHYLIB_ROLLING_BALL) 
            {
                if (phylib_stopped(new_table->object[i])) // Check if rolling ball has stopped
                {
                    stop = 1;
                }
                if (balls_bounced[i] == 1) // If ball has bounced, do not double bounce 
                {
                    continue;
                }
                for (int j = 0; j < PHYLIB_MAX_OBJECTS; j++) // Check if rolling ball has bounced into another object
                {
                    if (new_table->object[j] != NULL && i != j) 
                    {
                        distance = phylib_distance(new_table->object[i], new_table->object[j]);
                        if (distance < 0.0) 
                        {
                            stop = 1;
                            phylib_bounce(&new_table->object[i], &new_table->object[j]);
                            if (new_table->object[j]->type == PHYLIB_ROLLING_BALL) 
                            {
                                balls_bounced[j] = 1;
                            }
                            break;
                        }
                    }
                }
            }
        }
        if (stop) // Exit loop if a rolling ball has stopped or a ball has bounced
        {
            break;
        }
    }

    return new_table;

}

char *phylib_object_string( phylib_object *object )
{
    static char string[80];
    if (object==NULL)
    {
        snprintf( string, 80, "NULL;" );
        return string;
    }

    switch (object->type)
    {
    case PHYLIB_STILL_BALL:
        snprintf( string, 80,
                "STILL_BALL (%d,%6.1lf,%6.1lf)",
                object->obj.still_ball.number,
                object->obj.still_ball.pos.x,
                object->obj.still_ball.pos.y );
        break;

    case PHYLIB_ROLLING_BALL:
        snprintf( string, 80,
                "ROLLING_BALL (%d,%6.1lf,%6.1lf,%6.1lf,%6.1lf,%6.1lf,%6.1lf)",
                object->obj.rolling_ball.number,
                object->obj.rolling_ball.pos.x,
                object->obj.rolling_ball.pos.y,
                object->obj.rolling_ball.vel.x,
                object->obj.rolling_ball.vel.y,
                object->obj.rolling_ball.acc.x,
                object->obj.rolling_ball.acc.y );
        break;

    case PHYLIB_HOLE:
        snprintf( string, 80,
                "HOLE (%6.1lf,%6.1lf)",
                object->obj.hole.pos.x,
                object->obj.hole.pos.y );
    break;

    case PHYLIB_HCUSHION:
        snprintf( string, 80,
                "HCUSHION (%6.1lf)",
                object->obj.hcushion.y );
    break;

    case PHYLIB_VCUSHION:
        snprintf( string, 80,
                "VCUSHION (%6.1lf)",
                object->obj.vcushion.x );
    break;
    }
    return string;
}
