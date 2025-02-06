SOURCES := $(wildcard src/*.s)
OBJS := $(patsubst src/%.s,obj/%.o,$(SOURCES))

$(shell mkdir -p obj)

spctest.sfc: $(OBJS)
	ld65 -C ld65.cfg --dbgfile spctest.dbg -o $@ $(OBJS)

obj/%.o: src/%.s src/*.inc
	ca65 -g -o $@ $<

.PHONY: clean
clean:
	rm -rf obj/ spctest.sfc
