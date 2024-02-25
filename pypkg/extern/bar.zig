const print = @import("std").debug.print;
const c = @cImport({
    @cInclude("foo.h");
});

export fn bar(a: c_int, b: c_int) void {
    print("{d}\n", .{c.foo(a, b)});
}
