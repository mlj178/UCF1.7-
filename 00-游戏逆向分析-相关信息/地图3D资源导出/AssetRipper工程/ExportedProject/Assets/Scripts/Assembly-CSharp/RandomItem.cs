using System;
using System.Collections.Generic;

[Serializable]
public class RandomItem
{
	[Serializable]
	public struct Item
	{
		public string name;

		public int count;
	}

	public Item[] items;

	private List<int> idList;

	public void Init()
	{
	}

	public string Get()
	{
		return null;
	}
}
