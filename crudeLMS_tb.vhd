--Testbench for the crudeLMS module
--Can probably be repurposed for virtually all LMS modules!
library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

use std.textio.all;


entity crudeLMS_tb is
end crudeLMS_tb;

architecture tb of crudeLMS_tb is

	component crudeLMS is
		generic (g_width 	: integer:=12;
			g_mu		: integer:=5);
		port (	i_clk 	: in std_logic;
			i_reset	: in std_logic;
			i_refere	: in signed (g_width-1 downto 0);
			i_contam : in signed (g_width-1 downto 0);
			o_debug	: out signed (g_width-1 downto 0);
			o_output	: out signed (g_width-1 downto 0));
	end component;
	
	constant c_period : time:=25ns;
	constant c_width	: integer:=12;
	constant c_mu		: integer:=5;
	
	signal r_clk 		: std_logic;
	signal w_reset		: std_logic:='1';
	signal w_refere 	: signed(c_width-1 downto 0);
	signal w_contam 	: signed(c_width-1 downto 0);
	signal w_output	: signed(c_width-1 downto 0);
	signal w_debug		: signed(c_width-1 downto 0);
	
	file f_data : text;
	
begin
	
	UUT: crudeLMS
		generic map (g_width=>c_width)
		port map (i_clk=>r_clk, i_reset=>w_reset,
					 i_refere=>w_refere, i_contam=>w_contam,
					 o_output=>w_output, o_debug=>w_debug);
	
	TEST: process
		variable v_dataLine : line;
		variable v_comma : character;
		variable v_contamInt : integer;
		variable v_refereInt	: integer;
	begin
	
		file_open(f_data, "C:/Users/Alexander Greer/Documents/dspPractice/simCSV/f_crudeLMS.csv", read_mode);

		while not endfile(f_data) loop
			readline(f_data, v_dataLine);
			if (v_dataLine'length /= 0) then
			
				read(v_dataline, v_refereInt);
				read(v_dataline, v_comma);
				read(v_dataline, v_contamInt);
				
				w_refere <= to_signed(v_refereInt, c_width);
				w_contam <= to_signed(v_contamInt, c_width);
				
				wait for c_period;
				r_clk <= '1';
				wait for c_period;
				r_clk <= '0';
				w_reset <= '0';
			end if;
		end loop;
		file_close(f_data);
		
	end process;
	
end tb;