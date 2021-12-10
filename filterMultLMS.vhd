--Basic LMS algo
--Will compare with signum later
--Fully pipelined 16 tap LMS algo;

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;


entity filterMultLMS is
	generic( g_width 	: integer:=16;		--must be a power of two
				g_mu		: integer := 6); 	--log
	port(		i_clk		: in std_logic;
				i_reset	: in std_logic;
				i_ref		: in signed(g_width-1 downto 0);
				i_contam : in signed(g_width-1 downto 0);
				o_error	: out signed(g_width-1 downto 0));
end filterMultLMS;


architecture arch of filterMultLMS is
	
	type t_coef is array (15 downto 0) of signed (g_width-1 downto 0);
	type t_last is array (23 downto 0) of signed (g_width-1 downto 0);
	type t_result is array (31 downto 0) of signed (g_width-1 downto 0);
	signal a_coef : t_coef;
	signal a_last : t_last;
	signal a_result : t_result;
	
begin
	
	MAIN: process (i_clk, i_reset, i_ref, i_contam) is
		variable v_sum : signed(g_wdith*2-1 downto 0) := i_ref;
	begin
	
		if (i_reset = '1') then
			for C in a_coef'range loop
				a_coef(C) <= (others=> '0');
			end loop;
			for L in a_last'range loop
				a_last(C) <= (others=> '0');
				a_result(C) <= (others => '0');
			end loop;
			
			
		elsif (rising_edge(i_clk)) then
			for C in 15 downto 1 loop
				a_result(C+16) <= a_coef(C) * a_last(C); --1
			end loop;
			a_result(16) <= a_coef(0)*i_ref;
			
			for C in 7 downto 0 loop
				a_result(C+8) <= a_result(C*2) + a_result(C*2+1); --2
			end loop;
				
			a_result(7) <= a_result(16) + a_result(15); --3
			a_result(6) <= a_result(14) + a_result(13);
			a_result(5) <= a_result(12) + a_result(11);
			a_result(4) <= a_result(10) + a_result(9);
			
			a_result(3) <= a_result(7) + a_result(6); --4
			a_result(2) <= a_result(5) + a_result(4);
			
			a_result(1) <= a_result(3) + a_result(2); --5
			a_result(0) <= a_result(1) - i_contam; --6		
			o_error <= a_result(1) - i_contam;
			
			--then wap through again and update the coefficients
			--This could probably really use optimisation
			for C in 15 downto 0 loop
				a_coef(C) <= a_coef(C) + shift_left(a_result(C)*a_last(C+6), g_mu); 
			end loop;
			
			--praying for compiler optimisation
			for L in 23 downto 2 loop
				a_last(L) <= a_last(L-1); 
			end loop;
			a_last(1) <= i_ref; 
			
			
		end if;
		
	end process MAIN;

end arch;