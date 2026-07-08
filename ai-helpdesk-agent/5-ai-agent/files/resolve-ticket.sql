-- AI Tool: Execute Server-side Code -- resolve_ticket
-- Paste as the tool's PL/SQL source in Lab 5, Task 4.
-- :ticket_id is the tool parameter the agent fills from conversation context.
-- apex_ai.set_tool_result tells the agent what actually happened.
declare
  l_subject tickets.subject%type;
begin
  select subject into l_subject from tickets where id = :ticket_id;
  update tickets set status = 'Resolved' where id = :ticket_id;
  apex_ai.set_tool_result(
    p_result => 'Ticket ' || :ticket_id || ' ("' || l_subject || '") is now Resolved.');
exception
  when no_data_found then
    apex_ai.set_tool_result(p_result => 'No ticket with id ' || :ticket_id || ' exists.');
end;
