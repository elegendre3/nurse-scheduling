from pulp import (LpMinimize, LpProblem, LpStatus, lpSum, LpVariable)


## Define problem
prob = LpProblem("simpleScheduleProblem", LpMinimize)

## Define variables
# Schema: [person]_[floor]_[day_period]
a_a_1 = LpVariable('a_a_1', lowBound=0, upBound=1, cat='Integer')
a_a_2 = LpVariable('a_a_2', lowBound=0, upBound=1, cat='Integer')
a_b_1 = LpVariable('a_b_1', lowBound=0, upBound=1, cat='Integer')
a_b_2 = LpVariable('a_b_2', lowBound=0, upBound=1, cat='Integer')

b_a_1 = LpVariable('b_a_1', lowBound=0, upBound=1, cat='Integer')
b_a_2 = LpVariable('b_a_2', lowBound=0, upBound=1, cat='Integer')
b_b_1 = LpVariable('b_b_1', lowBound=0, upBound=1, cat='Integer')
b_b_2 = LpVariable('b_b_2', lowBound=0, upBound=1, cat='Integer')

c_a_1 = LpVariable('c_a_1', lowBound=0, upBound=1, cat='Integer')
c_a_2 = LpVariable('c_a_2', lowBound=0, upBound=1, cat='Integer')
c_b_1 = LpVariable('c_b_1', lowBound=0, upBound=1, cat='Integer')
c_b_2 = LpVariable('c_b_2', lowBound=0, upBound=1, cat='Integer')

## Define obj function
cost_func = lpSum(
    a_a_1 + a_a_2 + a_b_1 + a_b_2 +
    2 * (b_a_1 + b_a_2) + b_b_1 + b_b_2 +  # skewing towards b NOT being on floor "a"
    c_a_1 + c_a_2 + c_b_1 + c_b_2
)
prob += cost_func

## Define Constraints

# Enough staffing per floor
floor_a_1 = lpSum(a_a_1 + b_a_1 + c_a_1) >= 2.0
floor_a_2 = lpSum(a_a_2 + b_a_2 + c_a_2) >= 2.0
floor_b_1 = lpSum(a_b_1 + b_b_1 + c_b_1) >= 1.0
floor_b_2 = lpSum(a_b_2 + b_b_2 + c_b_2) >= 1.0
prob += floor_a_1
prob += floor_a_2
prob += floor_b_1
prob += floor_b_2

# Max Day
day_max_a = lpSum(a_a_1 + a_a_2 + a_b_1 + a_b_2) <= 2.0
day_max_b = lpSum(b_a_1 + b_a_2 + b_b_1 + b_b_2) <= 2.0
day_max_c = lpSum(c_a_1 + c_a_2 + c_b_1 + c_b_2) <= 2.0
prob += day_max_a
prob += day_max_b
prob += day_max_c

# Can't be in more than 1 place
unicity_a_1 = lpSum(a_a_1 + a_b_1) <= 1.0
unicity_a_2 = lpSum(a_a_2 + a_b_2) <= 1.0
unicity_b_1 = lpSum(b_a_1 + b_b_1) <= 1.0
unicity_b_2 = lpSum(b_a_2 + b_b_2) <= 1.0
unicity_c_1 = lpSum(c_a_1 + c_b_1) <= 1.0
unicity_c_2 = lpSum(c_a_2 + c_b_2) <= 1.0
prob += unicity_a_1
prob += unicity_a_2
prob += unicity_b_1
prob += unicity_b_2
prob += unicity_c_1
prob += unicity_c_2


# Incompatibilities
#todo

# Solve
prob.solve()
print(f"Status: [{LpStatus[prob.status]}]")

# Show solution
for v in prob.variables():
    if v.varValue > 0:
        print(v.name, "=", v.varValue)



###### ISSUES ######
# - not scalable
# - - in terms of making it for a bigger system
# - - in terms of adding new resources/constraints
