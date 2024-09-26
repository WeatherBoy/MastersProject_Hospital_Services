# NOTES: On how the current Regex pattern works

## New Regex Pattern:
```
pattern = r'^([^\s(]+(?:_[^\s(]+)?)\s*(?:\(([^)]+)\))?\s*(.*)$'
```

### Explanation of the Updated Regex Pattern:
- `^`: Asserts the start of the string.
- `([^\s(]+(?:_[^\s(]+)?)`: Group 1 captures the name, including optional initials or monikers after an underscore.
  - `[^\s(]+`: Matches one or more characters that are not whitespace or `(`.
  - `(?:_[^\s(]+)?`: Optionally matches an underscore followed by one or more characters that are not whitespace or `(`.
- `\s*`: Matches optional whitespace.
- `(?:\(([^)]+)\))?`: Group 2 optionally captures the timeslot within parentheses.
  - `\(` and `\)`: Match literal parentheses.
  - `([^)]+)`: Captures any characters except `)` (the timeslot).
- `\s*`: Matches optional whitespace.
- `(.*)$`: Group 3 captures the rest of the line as "Extra" information.
