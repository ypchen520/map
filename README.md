# Life Simulation Map

1. Pygame setup
2. Draw the timeline road
3. Character with animation and scaling
4. Progress
5. Task creation using the mouse
6. Make the character autonomous: move to the created task
7. Add milestones
8. Multiple characters
9. Give agents energy
   - Add an energy attribute to the Character class.
   - Update the agent's "brain" with new rules:
     - Moving costs energy.
     - Characters can only start a new task if they have enough energy.
     - If their energy is low, they will rest to recover it.
   - Add a visual energy bar below each character so we can see their status.