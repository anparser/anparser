rule test
{
    meta:
        author = "Preston Miller"
        description = "Test Rule"

	strings:
		$a = "hello"

	condition:
		$a
}