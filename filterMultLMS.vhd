--Basic LMS algo
--Will compare with signum later

--Pipelined LMS, but with a delay between coefficient update and 

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;


entity filterMultLMS is
	generic( g_width 	: integer:=16;	   
				g_noTaps : integer := 4;	--log
				g_mu		: integer := 4;); --log
	port(		i_clk		: in std_logic;
				i_reset	: in std_logic;
				i_ref		: in signed(g_width-1 downto 0);
				i_contam : in signed(g_width-1 downto 0);
				o_error	: out signed(g_width-1 downto 0));
end filterMultLMS;


architecture arch of filterMultLMS is
	
	type t_coef is array (g_noTaps-1 downto 0) of unsigned (g_width-1 downto 0);
	type t_last is array (g_noTaps-2 downto 0) of unsigned (g_width-1 downto 0);
	
	signal a_coef : t_coef;
	signal a_last : t_last;
	
begin
	
	MAIN: process (i_clk, i_reset, i_ref, i_contam) is
		variable sum : signed(g_wdith*2-1 downto 0);
	begin
	
		if (i_reset = '1') then
			for C in a_coef'range loop
				a_coef(C) <= (others=> '0');
			end loop;
			for L in a_last'range loop
				a_last(C) <= (others=> '0')
			end loop;
			
			
		elsif (rising_edge(i_clk)) then
			for C in a_last'range loop
				--Add sum to variable
			end loop;
			
			--then subtract i_contam
			
			--then wap through again and update the coefficients
		end if;
		
	end process MAIN;

end arch